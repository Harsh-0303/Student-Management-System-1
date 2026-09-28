from Data_layer.data_loader import load_all_data


def create_user_movie_matrix():
    movies, ratings, links = load_all_data()

    user_movie_matrix = ratings.pivot_table(
        index="userId",
        columns="movieId",
        values="rating",
        fill_value=0
    )

    return user_movie_matrix