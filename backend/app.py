import os
import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from services.llm_service import analyze_query
from services.tmdb_service import search_tmdb, get_movie_details
from models.schemas import SearchRequest
from utils.rate_limit import is_allowed

load_dotenv()

app = FastAPI()

# --- CORS SETUP ---

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/search")
def search_movies(req: SearchRequest, request: Request):
    # On Render, the real user IP is in the 'X-Forwarded-For' header.
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        client_ip = forwarded.split(",")[0]
    else:
        client_ip = request.client.host or "unknown"

    if not is_allowed(client_ip):
        raise HTTPException(
            status_code=429,
            detail="Too many search requests. Please slow down and try again.",
        )

    # --- LLM + TMDB search flow ---
    analysis = analyze_query(req.query)
    
    # Simple fallback: if title found, use it; otherwise use raw query
    search_term = analysis["titles"][0] if analysis.get("titles") else req.query
    
    movies = search_tmdb({"query": search_term})
    
    return {"results": movies, "analysis": analysis}


@app.get("/api/movies/{movie_id}")
def movie_detail(movie_id: int):
    return get_movie_details(movie_id)

# --- SERVER ENTRY POINT ---

if __name__ == "__main__":
    # Render provides the PORT env variable. Default to 10000 or 4000 locally.
    port = int(os.environ.get("PORT", 4000))
    uvicorn.run("app:app", host="0.0.0.0", port=port)