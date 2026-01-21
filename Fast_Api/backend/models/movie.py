# backend/models/movie.py
from pydantic import BaseModel

class Movie(BaseModel):
    title: str
    rating: float
    year: int
    genre: str
    country: str
    director: str