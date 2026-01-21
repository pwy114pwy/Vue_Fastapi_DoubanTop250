# backend/api/v1/chart.py
from fastapi import APIRouter
from collections import Counter
from ...services.data_loader import load_movies

router = APIRouter()

@router.get("/rating-distribution")
def get_rating_distribution():
    movies = load_movies()
    print(movies)
    # 统计 9.0~10.0, 8.0~9.0, ..., 0.0~1.0（共10个区间）
    bins = [0] * 10
    labels = [f"{i}.0-{i+1}.0" for i in range(10)]
    for m in movies:
        idx = min(int(m.rating), 9)  # 9.7 → 9, 10.0 → 9
        bins[idx] += 1
    return {"x": labels, "y": bins}

@router.get("/genre-count")
def get_genre_count():
    movies = load_movies()
    all_genres = [g for movie in movies for g in movie.genres]
    counter = Counter(all_genres)
    # 取前10
    most_common = counter.most_common(10)
    genres, counts = zip(*most_common) if most_common else ([], [])
    return {"genres": list(genres), "counts": list(counts)}

@router.get("/year-trend")
def get_year_trend():
    movies = load_movies()
    years = [m.year for m in movies if 1900 <= m.year <= 2025]
    counter = Counter(years)
    # 按年份排序
    sorted_items = sorted(counter.items())
    if not sorted_items:
        return {"years": [], "counts": []}
    years, counts = zip(*sorted_items)
    return {"years": list(years), "counts": list(counts)}