import os
import requests

from .parser_service import normalize_movie
from utils.error_handler import safe_raise
from dotenv import load_dotenv


# Load environment variables from .env (backend/.env)
load_dotenv()

BASE = "https://api.themoviedb.org/3"

TMDB_API_KEY = os.getenv("TMDB_API_KEY")

if not TMDB_API_KEY:
    raise RuntimeError(
        "TMDB_API_KEY is not set. "
        "Add TMDB_API_KEY=<your_v3_api_key> in backend/.env"
    )


def search_tmdb(params: dict):
    """
    Basic TMDB search by title/keywords using v3 API key.
    """
    query = params["query"]

    try:
        r = requests.get(
            f"{BASE}/search/movie",
            params={
                "api_key": TMDB_API_KEY,
                "query": query,
                "include_adult": "false",
                "language": "en-US",
                "page": 1,
            },
            timeout=10,  # seconds
        )
    except requests.exceptions.Timeout:
        # 504 = upstream timeout
        safe_raise(504, "TMDB request timed out. Please try again.")
    except requests.RequestException as e:
        # 502 = upstream failure
        safe_raise(502, f"TMDB request failed: {e}")

    if r.status_code != 200:
        safe_raise(502, f"TMDB returned {r.status_code}: {r.text}")

    data = r.json()
    return [normalize_movie(m) for m in data.get("results", [])]


def get_movie_details(movie_id: int):
    try:
        r = requests.get(
            f"{BASE}/movie/{movie_id}",
            params={
                "api_key": TMDB_API_KEY,
                "append_to_response": "credits,videos",
                "language": "en-US",
            },
            timeout=10,
        )
    except requests.exceptions.Timeout:
        safe_raise(504, "TMDB details request timed out.")
    except requests.RequestException as e:
        safe_raise(502, f"TMDB details request failed: {e}")

    if r.status_code == 404:
        safe_raise(404, "Movie not found")
    if r.status_code != 200:
        safe_raise(502, f"TMDB returned {r.status_code}: {r.text}")

    data = r.json()

    trailer_key = None
    for v in data.get("videos", {}).get("results", []):
        if v.get("site") == "YouTube" and v.get("type") == "Trailer":
            trailer_key = v["key"]
            break

    return {
        "id": data["id"],
        "title": data.get("title") or data.get("name", ""),
        "overview": data.get("overview", ""),
        "genres": [g["name"] for g in data.get("genres", [])],
        "poster": (
            f"https://image.tmdb.org/t/p/w500{data['poster_path']}"
            if data.get("poster_path")
            else None
        ),
        "trailer": f"https://www.youtube.com/watch?v={trailer_key}" if trailer_key else None,
        "cast": [c["name"] for c in data.get("credits", {}).get("cast", [])[:10]],
        "director": next(
            (c["name"] for c in data.get("credits", {}).get("crew", []) if c.get("job") == "Director"),
            None,
        ),
    }
