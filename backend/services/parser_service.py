def normalize_movie(m):
    return {
        "id": m["id"],
        "title": m["title"],
        "release_year": m.get("release_date", "")[:4],
        "rating": m.get("vote_average"),
        "poster": f"https://image.tmdb.org/t/p/w342{m['poster_path']}" if m.get("poster_path") else None
    }
