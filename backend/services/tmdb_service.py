import os
import time
import requests
from typing import Dict, List, Tuple, Optional

from .parser_service import normalize_movie
from utils.error_handler import safe_raise
from dotenv import load_dotenv

load_dotenv()

BASE = "https://api.themoviedb.org/3"

TMDB_API_KEY = os.getenv("TMDB_API_KEY")

if not TMDB_API_KEY:
    raise RuntimeError(
        "TMDB_API_KEY is not set. "
        "Add TMDB_API_KEY=<your_v3_api_key> in backend/.env"
    )

# -------------------------------
# Simple in-memory caches
# -------------------------------

# Cache for search results: query -> (expires_at, [movies])
_SEARCH_TTL_SECONDS = 60  # 1 minute cache for search results
_search_cache: Dict[str, Tuple[float, List[dict]]] = {}

# Cache for movie details: movie_id -> (expires_at, details)
_DETAILS_TTL_SECONDS = 300  # 5 minutes cache for details
_details_cache: Dict[int, Tuple[float, dict]] = {}


def _get_from_search_cache(query_key: str) -> Optional[List[dict]]:
    entry = _search_cache.get(query_key)
    if not entry:
        return None
    expires_at, data = entry
    if time.time() > expires_at:
        # expired, drop it
        _search_cache.pop(query_key, None)
        return None
    return data


def _set_search_cache(query_key: str, data: List[dict]):
    _search_cache[query_key] = (time.time() + _SEARCH_TTL_SECONDS, data)


def _get_from_details_cache(movie_id: int) -> Optional[dict]:
    entry = _details_cache.get(movie_id)
    if not entry:
        return None
    expires_at, data = entry
    if time.time() > expires_at:
        _details_cache.pop(movie_id, None)
        return None
    return data


def _set_details_cache(movie_id: int, data: dict):
    _details_cache[movie_id] = (time.time() + _DETAILS_TTL_SECONDS, data)


def search_tmdb(params: dict):
    """
    Basic TMDB search by title/keywords using v3 API key.
    Adds a small in-memory cache to avoid hammering TMDB for identical queries.
    """
    raw_query = params["query"]
    query = raw_query.strip().lower()

    # 1) Try cache first
    cached = _get_from_search_cache(query)
    if cached is not None:
        return cached

    # 2) Call TMDB if not cached
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
    results = [normalize_movie(m) for m in data.get("results", [])]

    # 3) Store in cache
    _set_search_cache(query, results)

    return results


def get_movie_details(movie_id: int):
    # 1) Try cache first
    cached = _get_from_details_cache(movie_id)
    if cached is not None:
        return cached

    # 2) Fetch from TMDB
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

    details = {
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

    # 3) Cache details
    _set_details_cache(movie_id, details)

    return details
