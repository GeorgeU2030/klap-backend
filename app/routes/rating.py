from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.rating_schema import RatingCreate, RatingResponse
from app.services.rating_service import RatingService
from app.database import get_db
from app.models.rating_model import Rating

router = APIRouter(prefix="/rating", tags=["Rating"])

@router.post("/create", response_model=RatingResponse, status_code=status.HTTP_201_CREATED)
def create_rating(request: RatingCreate, db: Session = Depends(get_db)):
    total_score = RatingService.calculate_total_score(request)
    item_id = RatingService.find_or_create_item(db, request, new_rating_total_score=total_score)

    if RatingService.has_user_rated_item(db, request.user_id, item_id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User has already rated this item"
        )

    rating = RatingService.create_rating(db, request, item_id)
    return rating

@router.get("/get/{user_id}/{item_id}", response_model=RatingResponse)
def get_rating(user_id: int, item_id: int, db: Session = Depends(get_db)):
    rating = db.query(Rating).filter(Rating.user_id == user_id, Rating.item_id == item_id).first()
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    return rating

@router.put("/update/{user_id}/{item_id}")
def update_rating(user_id: int, item_id: int, rating_data: RatingCreate, db: Session = Depends(get_db)):
    rating = db.query(Rating).filter(Rating.user_id == user_id, Rating.item_id == item_id).first()
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    for field, value in rating_data.dict().items():
        setattr(rating, field, value)
    rating.total_score = (
        rating.story + rating.direction + rating.performances +
        rating.visuals + rating.sound + rating.emotion + rating.rewatch
    )
    db.commit()
    db.refresh(rating)
    return {"message": "Rating updated"}



