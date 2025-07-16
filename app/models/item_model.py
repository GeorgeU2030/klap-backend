from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.database import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tmdb_id = Column(Integer, nullable=False)
    type = Column(String, nullable=False)
    original_title = Column(String, nullable=False)
    overview = Column(Text, nullable=False)
    poster_path = Column(String, nullable=False)
    release_date = Column(String, nullable=False)
    vote_average = Column(Integer, nullable=False)
    vote_count = Column(Integer, nullable=False)
    backdrop_path = Column(String, nullable=True)
    genres = Column(Text, nullable=False)
    number_of_seasons = Column(Integer, nullable=False, default=0)

    ratings = relationship("Rating", back_populates="item")