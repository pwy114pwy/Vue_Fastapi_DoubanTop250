# backend/models/movie.py
from pydantic import BaseModel
from typing import List

class Movie(BaseModel):
    title: str
    rating: float
    year: int
    genres: List[str]
    country: str
    director: str