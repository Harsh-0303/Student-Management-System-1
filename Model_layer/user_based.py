import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

from Database.queries import (
    get_all_ratings_for_recommendation,
    get_all_movies_for_recommendation
)


def calculate_user_similarity():
    rating_data = get_all_ratings_for_recommendation()

    ratings = pd.DataFrame(
        rating_data,
        columns=["userId", "movieId", "rating"]
    )

    user_movie_matrix = ratings.pivot_table(
        index="userId",
        columns="movieId",
        values="rating",
        fill_value=0
    )

    similarity_matrix = cosine_similarity(user_movie_matrix)

    return similarity_matrix, user_movie_matrix



def get_user_recommendations(user_id, top_n=10):

    rating_data = get_all_ratings_for_recommendation()
    movie_data = get_all_movies_for_recommendation()

    ratings = pd.DataFrame(
        rating_data,
        columns=["userId", "movieId", "rating"]
    )

    movies = pd.DataFrame(
        movie_data,
        columns=["movieId", "title"]
    )

    similarity_matrix, user_movie_matrix = calculate_user_similarity()

    if user_id not in user_movie_matrix.index:
        raise ValueError("User ID not found")

    user_index = user_movie_matrix.index.get_loc(user_id)

    similarities = similarity_matrix[user_index]

    similar_users = (
        pd.Series(
            similarities,
            index=user_movie_matrix.index
        )
        .sort_values(ascending=False)
    )

    similar_users = similar_users.drop(user_id).head(5)

    watched_movies = ratings[
        ratings["userId"] == user_id
    ]["movieId"].tolist()

    recommendations = ratings[
        ratings["userId"].isin(similar_users.index)
    ]

    recommendations = recommendations[
        ~recommendations["movieId"].isin(watched_movies)
    ]

    recommendations = (
        recommendations
        .groupby("movieId")["rating"]
        .mean()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index()
    )

    recommendations = recommendations.merge(
        movies,
        on="movieId"
    )

    return recommendations[
        ["movieId", "title", "rating"]
    ]

if __name__ == "__main__":
    recommendations = get_user_recommendations(user_id=1)

    print("\nRecommendations for User 1:\n")

    for index, row in recommendations.iterrows():
        print(
            f"{index + 1}. {row['title']} "
            f"(Movie ID: {row['movieId']}) "
            f"- Rating: {row['rating']:.2f}"
        )