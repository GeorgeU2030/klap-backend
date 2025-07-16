from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base

class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)

    story = Column(Integer, nullable=False)
    direction = Column(Integer, nullable=False)
    performances = Column(Integer, nullable=False)
    visuals = Column(Integer, nullable=False)
    sound = Column(Integer, nullable=False)
    emotion = Column(Integer, nullable=False)
    rewatch = Column(Integer, nullable=False)
    total_score = Column(Integer, nullable=False)

    user = relationship("User", back_populates="ratings")
    item = relationship("Item", back_populates="ratings")