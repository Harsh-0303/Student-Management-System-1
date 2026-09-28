import pandas as pd

MOVIES_PATH = "Data_layer/movies.csv"
RATINGS_PATH = "Data_layer/ratings.csv"
LINKS_PATH = "Data_layer/links.csv"


def load_movies():
    movies = pd.read_csv(MOVIES_PATH)

    required_columns = [
        "movieId",
        "title",
        "genres"
    ]

    if not all(column in movies.columns for column in required_columns):
        raise ValueError("movies.csv has missing required columns.")

    return movies


def load_ratings():
    ratings = pd.read_csv(RATINGS_PATH)

    required_columns = [
        "userId",
        "movieId",
        "rating",
        "timestamp"
    ]

    if not all(column in ratings.columns for column in required_columns):
        raise ValueError("ratings.csv has missing required columns")

    return ratings


def load_links():
    links  = pd.read_csv(LINKS_PATH)

    required_columns = [
        "movieId",
        "imdbId",
        "tmdbId"
    ]

    if not all(column in links.columns for column in required_columns):
        raise ValueError("links.csv has missing required columns")

    return links


def load_all_data():
    movies = load_movies()
    ratings = load_ratings()
    links = load_links()

    return movies, ratings, links