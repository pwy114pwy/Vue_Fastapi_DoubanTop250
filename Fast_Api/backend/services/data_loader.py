# backend/services/data_loader.py
import json
from pathlib import Path
from typing import List
from ..models.movie import Movie

def load_movies() -> List[Movie]:
    # 定位到 backend/data/movies.json
    data_path = Path(__file__).parent.parent / "data" / "movies.json"
    with open(data_path, encoding="utf-8") as f:
        raw_data = json.load(f)
    return [Movie(**item) for item in raw_data]