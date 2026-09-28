import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Load data
movies = pd.read_csv("Data_layer/movies.csv")
ratings = pd.read_csv("Data_layer/ratings.csv")

# Create User-Movie Matrix
user_movie_matrix = ratings.pivot_table(
    index="userId",
    columns="movieId",
    values="rating",
    fill_value=0
)

# Calculate User Similarity
user_similarity = cosine_similarity(user_movie_matrix)


# Recommendation Function
def get_recommendations(user_id):

    # Movies already watched by user
    watched_movies = ratings[
        ratings["userId"] == user_id
    ]["movieId"].tolist()

    # Find similar users
    user_index = user_movie_matrix.index.get_loc(user_id)

    similarities = user_similarity[user_index]

    similar_users = pd.Series(
        similarities,
        index=user_movie_matrix.index
    )

    similar_users = similar_users.sort_values(
        ascending=False
    )

    similar_users = similar_users.drop(user_id).head(5)

    # Movies rated by similar users
    recommendations = ratings[
        ratings["userId"].isin(similar_users.index)
    ]

    # Remove already watched movies
    recommendations = recommendations[
        ~recommendations["movieId"].isin(watched_movies)
    ]

    # Calculate average rating
    recommendations = (
        recommendations
        .groupby("movieId")["rating"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
    )

    # Add movie titles
    recommendations = recommendations.reset_index()

    recommendations = recommendations.merge(
        movies,
        on="movieId"
    )

    return recommendations[[
        "movieId",
        "title",
        "rating"
    ]]

print(get_recommendations(1))