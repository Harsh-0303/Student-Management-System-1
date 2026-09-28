from fastapi import FastAPI

from Model_layer.user_based import get_user_recommendations
from Model_layer.item_based import get_item_recommendations


app = FastAPI(
    title="Movie Recommendation System API"
)


@app.get("/")
def home():
    return {
        "message": "Movie Recommendation System API is running"
    }


@app.get("/recommendations/user/{user_id}")
def user_recommendation(user_id: int):

    recommendations = get_user_recommendations(
        user_id=user_id
    )

    return recommendations.to_dict(
        orient="records"
    )


@app.get("/recommendations/movie/{movie_id}")
def movie_recommendation(movie_id: int):

    recommendations = get_item_recommendations(
        movie_id=movie_id
    )

    return recommendations.to_dict(
        orient="records"
    )