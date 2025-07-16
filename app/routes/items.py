from ast import literal_eval
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.item_model import Item
from app.database import get_db
from app.schemas.rating_schema import ItemResponse

router = APIRouter(prefix="/items", tags=["Item"])

@router.get("/search", response_model=List[ItemResponse])
def search_items_by_title(title: str, db: Session = Depends(get_db)):
    items = db.query(Item).filter(Item.original_title.ilike(f"%{title}%")).all()

    response = []
    for item in items:
        genres_list = literal_eval(item.genres) if item.genres else []
        genres = [{"id": index + 1, "name": name} for index, name in enumerate(genres_list)]

        response.append({
            "id": item.id,
            "tmdb_id": item.tmdb_id,
            "type": item.type,
            "original_title": item.original_title,
            "overview": item.overview,
            "poster_path": item.poster_path,
            "release_date": item.release_date,
            "vote_average": item.vote_average,
            "backdrop_path": item.backdrop_path,
            "vote_count": item.vote_count,
            "number_of_seasons": item.number_of_seasons,
            "genres": genres
        })

    return response



@router.get("/{type}/{id}", response_model=ItemResponse)
def get_item_by_tmdb_id(type: str, id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == id, Item.type == type).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    genres_list = literal_eval(item.genres) if item.genres else []
    item.genres = [{"id": index + 1, "name": name} for index, name in enumerate(genres_list)]

    return item

