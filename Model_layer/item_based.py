import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

from Database.queries import (
    get_all_ratings_for_recommendation,
    get_all_movies_for_recommendation
)


def calculate_item_similarity():

    rating_data = get_all_ratings_for_recommendation()

    ratings = pd.DataFrame(
        rating_data,
        columns=["userId", "movieId", "rating"]
    )

    movie_user_matrix = ratings.pivot_table(
        index="movieId",
        columns="userId",
        values="rating",
        fill_value=0
    )

    similarity_matrix = cosine_similarity(movie_user_matrix)

    return similarity_matrix, movie_user_matrix


def get_item_recommendations(movie_id, top_n=10):

    movie_data = get_all_movies_for_recommendation()

    movies = pd.DataFrame(
        movie_data,
        columns=["movieId", "title"]
    )

    similarity_matrix, movie_user_matrix = calculate_item_similarity()

    if movie_id not in movie_user_matrix.index:
        raise ValueError("Movie ID not found")

    movie_index = movie_user_matrix.index.get_loc(movie_id)

    similarities = similarity_matrix[movie_index]

    similar_movies = (
        pd.Series(
            similarities,
            index=movie_user_matrix.index
        )
        .sort_values(ascending=False)
    )

    similar_movies = similar_movies.drop(movie_id).head(top_n)

    recommendations = pd.DataFrame({
        "movieId": similar_movies.index,
        "similarity": similar_movies.values
    })

    recommendations = recommendations.merge(
        movies,
        on="movieId"
    )

    return recommendations[
        ["movieId", "title", "similarity"]
    ]


if __name__ == "__main__":

    movie_id = 1

    recommendations = get_item_recommendations(
        movie_id=movie_id,
        top_n=10
    )

    print(f"\nMovies similar to Movie ID {movie_id}:\n")

    for index, row in recommendations.iterrows():
        print(
            f"{index + 1}. {row['title']} "
            f"(Movie ID: {row['movieId']}) "
            f"- Similarity: {row['similarity']:.4f}"
        )