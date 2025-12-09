from fastapi import FastAPI
from services.llm_service import analyze_query
from services.tmdb_service import search_tmdb, get_movie_details
from models.schemas import SearchRequest
from dotenv import load_dotenv
load_dotenv()
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # or ["*"] during dev if you want to be lazy
    allow_credentials=True,
    allow_methods=["*"],            
    allow_headers=["*"],
)
@app.post("/api/search")
def search_movies(req: SearchRequest):
    analysis = analyze_query(req.query)
    movies = search_tmdb({"query": analysis["titles"][0] if analysis["titles"] else req.query})
    return {"results": movies, "analysis": analysis}

@app.get("/api/movies/{movie_id}")
def movie_detail(movie_id: int):
    return get_movie_details(movie_id)
