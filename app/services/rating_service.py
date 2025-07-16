from sqlalchemy.orm import Session
from app.models.rating_model import Rating
from app.models.item_model import Item
from app.schemas.rating_schema import ItemData, RatingData

class RatingService:
    @staticmethod
    def find_or_create_item(db: Session, item_data: ItemData, new_rating_total_score: int = None) -> int:
        item = db.query(Item).filter(
            Item.tmdb_id == item_data.tmdb_id,
            Item.type == item_data.type
        ).first()
        if item:
            if new_rating_total_score is not None:
                new_vote_count = item.vote_count + 1
                item.vote_average = (item.vote_average * item.vote_count + new_rating_total_score) / new_vote_count
                item.vote_count = new_vote_count
                db.commit()
                db.refresh(item)
            return item.id

        new_item = Item(
            tmdb_id=item_data.tmdb_id,
            type=item_data.type,
            original_title=item_data.original_title,
            overview=item_data.overview,
            poster_path=item_data.poster_path,
            release_date=item_data.release_date,
            vote_average=new_rating_total_score if new_rating_total_score is not None else 0,
            vote_count=1 if new_rating_total_score is not None else 0,
            number_of_seasons= item_data.number_of_seasons,
            backdrop_path=item_data.backdrop_path,
            genres=str(item_data.genres)
        )

        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return new_item.id

    @staticmethod
    def has_user_rated_item(db: Session, user_id: int, item_id: int) -> bool:
        return db.query(Rating).filter(Rating.user_id == user_id, Rating.item_id == item_id).first() is not None

    @staticmethod
    def calculate_total_score(scores: RatingData) -> int:
        return (
                scores.story +
                scores.direction +
                scores.performances +
                scores.visuals +
                scores.sound +
                scores.emotion +
                scores.rewatch
        )

    @staticmethod
    def create_rating(db: Session, rating_data: RatingData, item_id: int) -> Rating:
        total_score = RatingService.calculate_total_score(rating_data)
        rating = Rating(
            user_id=rating_data.user_id,
            item_id=item_id,
            story=rating_data.story,
            direction=rating_data.direction,
            performances=rating_data.performances,
            visuals=rating_data.visuals,
            sound=rating_data.sound,
            emotion=rating_data.emotion,
            rewatch=rating_data.rewatch,
            total_score=total_score
        )
        db.add(rating)
        db.commit()
        db.refresh(rating)
        return rating
