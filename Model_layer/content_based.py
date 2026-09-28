import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from Data_layer.data_loader import load_all_data


def create_genre_matrix():
    movies, ratings, links = load_all_data()

    movies = movies.copy()

    movies["genres"] = movies["genres"].fillna("")

    vectorizer = CountVectorizer(
        tokenizer=lambda x: x.split("|"),
        token_pattern=None
    )

    genre_matrix = vectorizer.fit_transform(
        movies["genres"]
    )

    return movies, genre_matrix


def get_similar_movies(movie_id, top_n=10):
    movies, genre_matrix = create_genre_matrix()

    if movie_id not in movies["movieId"].values:
        raise ValueError("Movie ID not found")

    movie_index = movies.index[
        movies["movieId"] == movie_id
    ][0]

    similarity_scores = cosine_similarity(
        genre_matrix[movie_index],
        genre_matrix
    ).flatten()

    similar_movie_indices = (
        similarity_scores
        .argsort()[::-1]
    )

    similar_movie_indices = [
        index
        for index in similar_movie_indices
        if index != movie_index
    ][:top_n]

    recommendations = movies.iloc[
        similar_movie_indices
    ].copy()

    recommendations["similarity"] = (
        similarity_scores[similar_movie_indices]
    )

    return recommendations[
        ["movieId", "title", "genres", "similarity"]
    ]