from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=True)
    full_name = Column(String)
    profile_image = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_oauth = Column(Boolean, default=False)
    google_id = Column(String, nullable=True)

    ratings = relationship("Rating", back_populates="user")
