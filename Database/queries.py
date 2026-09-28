from sqlalchemy import func

from Database.database import SessionLocal
from Database.models import User, Movie, Rating



def get_movie(movie_id):
    session = SessionLocal()

    try:
        movie = session.query(Movie).filter(
            Movie.movie_id == movie_id
        ).first()

        return movie

    finally:
        session.close()


def get_user_ratings(user_id):
    session = SessionLocal()

    try:
        ratings = session.query(Rating).filter(
            Rating.user_id == user_id
        ).all()

        return ratings

    finally:
        session.close()


def get_movie_ratings(movie_id):
    session = SessionLocal()

    try:
        ratings = session.query(Rating).filter(
            Rating.movie_id == movie_id
        ).all()

        return ratings

    finally:
        session.close()


def get_movie_average_rating(movie_id):
    session = SessionLocal()

    try:
        ratings = session.query(Rating).filter(
            Rating.movie_id == movie_id
        ).all()

        if not ratings:
            return None

        total = sum(rating.rating for rating in ratings)

        average = total / len(ratings)

        return average

    finally:
        session.close()



def get_most_rated_movies(limit=10):
    session = SessionLocal()

    try:
        movies = (
            session.query(
                Movie.movie_id,
                Movie.title
            )
            .join(
                Rating,
                Movie.movie_id == Rating.movie_id
            )
            .all()
        )

        rating_counts = {}

        for movie_id, title in movies:

            if movie_id not in rating_counts:
                rating_counts[movie_id] = {
                    "movie_id": movie_id,
                    "title": title,
                    "rating_count": 0
                }

            rating_counts[movie_id]["rating_count"] += 1

        result = list(rating_counts.values())

        result.sort(
            key=lambda movie: movie["rating_count"],
            reverse=True
        )

        return result[:limit]

    finally:
        session.close()



def get_user_ratings_with_movies(user_id):
    session = SessionLocal()

    try:
        results = (
            session.query(
                Rating.user_id,
                Rating.movie_id,
                Rating.rating,
                Movie.title
            )
            .join(
                Movie,
                Rating.movie_id == Movie.movie_id
            )
            .filter(
                Rating.user_id == user_id
            )
            .all()
        )

        return results

    finally:
        session.close()


def get_all_ratings_for_recommendation():
    session = SessionLocal()

    try:
        results = (
            session.query(
                Rating.user_id,
                Rating.movie_id,
                Rating.rating
            )
            .all()
        )

        return results

    finally:
        session.close()



def get_all_movies_for_recommendation():
    session = SessionLocal()

    try:
        movies = (
            session.query(
                Movie.movie_id,
                Movie.title
            )
            .all()
        )

        return movies

    finally:
        session.close()



def get_total_ratings():
    session = SessionLocal()

    try:
        return session.query(Rating).count()

    finally:
        session.close()



def get_total_users():
    session = SessionLocal()

    try:
        return session.query(User).count()

    finally:
        session.close()



def get_total_movies():
    session = SessionLocal()

    try:
        return session.query(Movie).count()

    finally:
        session.close()



def get_average_rating():
    session = SessionLocal()

    try:
        ratings = session.query(Rating).all()

        if not ratings:
            return 0

        total = sum(rating.rating for rating in ratings)

        average = total / len(ratings)

        return average

    finally:
        session.close()


def get_rating_distribution():
    session = SessionLocal()

    try:
        ratings = session.query(Rating).all()

        distribution = {}

        for rating in ratings:

            value = rating.rating

            if value not in distribution:
                distribution[value] = 0

            distribution[value] += 1

        return distribution

    finally:
        session.close()


# =========================================
# DASHBOARD - TOP 10 HIGHEST RATED MOVIES
# =========================================

def get_highest_rated_movies(limit=10):

    session = SessionLocal()

    try:

        movies = (
            session.query(
                Movie.movie_id,
                Movie.title,
                func.avg(Rating.rating).label("average_rating"),
                func.count(Rating.rating).label("rating_count")
            )
            .join(
                Rating,
                Movie.movie_id == Rating.movie_id
            )
            .group_by(
                Movie.movie_id,
                Movie.title
            )
            .order_by(
                func.avg(Rating.rating).desc()
            )
            .limit(limit)
            .all()
        )

        result = []

        for movie in movies:

            result.append({
                "movie_id": movie.movie_id,
                "title": movie.title,
                "average_rating": round(
                    float(movie.average_rating),
                    2
                ),
                "rating_count": movie.rating_count
            })

        return result

    finally:

        session.close()