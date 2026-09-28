import pandas as pd

from Database.database import SessionLocal
from Database.models import Movie


LINKS_FILE = "Data_layer/links.csv"


def load_links(session):
    print("Loading links...")

    links_df = pd.read_csv(LINKS_FILE)

    updated_movies = 0

    for _, row in links_df.iterrows():

        movie = session.query(Movie).filter(
            Movie.movie_id == int(row["movieId"])
        ).first()

        if movie:
            movie.imdb_id = str(row["imdbId"])
            movie.tmdb_id = str(row["tmdbId"])

            updated_movies += 1

    session.commit()

    print(f"{updated_movies} movies updated with IMDb and TMDB IDs.")


def main():
    session = SessionLocal()

    try:
        load_links(session)

        print("Links data loaded successfully!")

    except Exception as error:
        session.rollback()

        print("Error while loading links:")
        print(error)

    finally:
        session.close()


if __name__ == "__main__":
    main()