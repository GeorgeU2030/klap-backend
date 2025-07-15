from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.user_schema import UserUpdate, UserResponse
from app.auth.dependencies import get_current_user
from app.database import get_db
from app.models.user_model import User

router = APIRouter(tags=["Users"])

@router.get("/user/me", response_model=UserResponse)
def read_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/user/me", response_model=UserResponse)
def update_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if user_update.full_name:
        current_user.full_name = user_update.full_name
    if user_update.profile_image:
        current_user.profile_image = user_update.profile_image

    db.commit()
    db.refresh(current_user)
    return current_user
