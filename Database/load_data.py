import pandas as pd

from Database.database import SessionLocal
from Database.models import User, Movie, Rating


# CSV file paths
MOVIES_FILE = "Data_layer/movies.csv"
RATINGS_FILE = "Data_layer/ratings.csv"


def load_movies(session):
    print("Loading movies....")

    movies_df = pd.read_csv(MOVIES_FILE)

    movies = []

    for _, row in movies_df.iterrows():
        movie = Movie(
            movie_id=int(row["movieId"]),
            title=row["title"],
            genres=row["genres"]
        )

        movies.append(movie)

    session.add_all(movies)
    session.commit()

    print(f"{len(movies)} movies loaded.")


def load_ratings(session):
    print("Loading ratings....")

    ratings_df = pd.read_csv(RATINGS_FILE)

    # Create users first
    user_ids = ratings_df["userId"].unique()

    users = []

    for user_id in user_ids:
        user = User(
            user_id=int(user_id)
        )

        users.append(user)

    session.add_all(users)
    session.commit()

    print(f"{len(users)} users loaded.")

    # Create ratings
    ratings = []

    for _, row in ratings_df.iterrows():
        rating = Rating(
            user_id=int(row["userId"]),
            movie_id=int(row["movieId"]),
            rating=float(row["rating"]),
            timestamp=int(row["timestamp"])
        )

        ratings.append(rating)

    session.add_all(ratings)
    session.commit()

    print(f"{len(ratings)} ratings loaded.")


def main():
    session = SessionLocal()

    try:
        load_movies(session)
        load_ratings(session)

        print("Data loading completed successfully!")

    except Exception as error:
        session.rollback()

        print("Error while loading data:")
        print(error)

    finally:
        session.close()


if __name__ == "__main__":
    main()