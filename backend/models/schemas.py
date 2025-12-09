from pydantic import BaseModel
from typing import List, Optional

class SearchRequest(BaseModel):
    query: str

class Movie(BaseModel):
    id: int
    title: str
    poster: Optional[str] = None
    release_year: Optional[str]
    rating: Optional[float]

class MovieDetail(BaseModel):
    id: int
    title: str
    overview: str
    genres: List[str]
    cast: List[str]
    director: Optional[str]
    trailer: Optional[str]
    poster: Optional[str]
