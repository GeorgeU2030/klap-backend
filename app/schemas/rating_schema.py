from pydantic import BaseModel, Field
from typing import List, Optional


class ItemData(BaseModel):
    tmdb_id: int
    type: str
    original_title: str
    overview: str
    poster_path: str
    release_date: str
    vote_average: int
    vote_count: int
    number_of_seasons: int
    backdrop_path: str
    genres: List[str]

class Genre(BaseModel):
    id: int
    name: str

class ItemResponse(BaseModel):
    id: int
    tmdb_id: int
    type: str
    original_title: str
    overview: str
    poster_path: Optional[str]
    release_date: Optional[str]
    vote_average: float
    vote_count: int
    backdrop_path: Optional[str]
    number_of_seasons: Optional[int]
    genres: List[Genre]

class RatingData(BaseModel):
    user_id: int
    story: int = Field(...)
    direction: int = Field(...)
    performances: int = Field(...)
    visuals: int = Field(...)
    sound: int = Field(...)
    emotion: int = Field(...)
    rewatch: int = Field(...)

class RatingCreate(ItemData, RatingData):
    pass

class RatingResponse(BaseModel):
    id: int
    user_id: int
    item_id: int
    story: int
    direction: int
    performances: int
    visuals: int
    sound: int
    emotion: int
    rewatch: int
    total_score: int
