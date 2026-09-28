from sqlalchemy import Column, Integer, String, Float, BigInteger, ForeignKey
from sqlalchemy.orm import relationship

from Database.database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)

    ratings = relationship(
        "Rating",
        back_populates="user"
    )


class Movie(Base):
    __tablename__ = "movies"

    movie_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    genres = Column(String, nullable=True)
    imdb_id = Column(String, nullable=True)
    tmdb_id = Column(String, nullable=True)

    ratings = relationship(
        "Rating",
        back_populates="movie"
    )


class Rating(Base):
    __tablename__ = "ratings"

    user_id = Column(
        Integer,
        ForeignKey("users.user_id"),
        primary_key=True
    )

    movie_id = Column(
        Integer,
        ForeignKey("movies.movie_id"),
        primary_key=True
    )

    rating = Column(Float, nullable=False)
    timestamp = Column(BigInteger, nullable=True)

    user = relationship(
        "User",
        back_populates="ratings"
    )

    movie = relationship(
        "Movie",
        back_populates="ratings"
    )