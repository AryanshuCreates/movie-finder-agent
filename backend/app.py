from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from services.llm_service import analyze_query
from services.tmdb_service import search_tmdb, get_movie_details
from models.schemas import SearchRequest
from utils.rate_limit import is_allowed

load_dotenv()

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/search")
def search_movies(req: SearchRequest, request: Request):
    # --- lightweight IP-based rate limiting ---
    client_ip = request.client.host or "unknown"

    if not is_allowed(client_ip):
        raise HTTPException(
            status_code=429,
            detail="Too many search requests. Please slow down and try again.",
        )

    # --- LLM + TMDB search flow ---
    analysis = analyze_query(req.query)
    movies = search_tmdb(
        {"query": analysis["titles"][0] if analysis["titles"] else req.query}
    )
    return {"results": movies, "analysis": analysis}


@app.get("/api/movies/{movie_id}")
def movie_detail(movie_id: int):
    return get_movie_details(movie_id)
