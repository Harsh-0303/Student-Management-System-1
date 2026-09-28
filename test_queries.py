from Database.queries import(
    get_movie,
    get_user_ratings,
    get_movie_ratings,
    get_movie_average_rating,
    get_most_rated_movies,
    get_user_ratings_with_movies,
    get_all_ratings_for_recommendation
)



# =============================
# TEST 1: GET MOVIE
# =============================

movie =get_movie(1)

print("\nMovie:")
print(movie.title)
print(movie.genres)



# =============================
# TEST 2: GET RATINGS
# =============================

ratings = get_user_ratings(1)

print("\nUser 1 Ratings:")
print("Total ratings:", len(ratings))

for rating in ratings[:5]:
    print(
        "Movie ID:",
        rating.movie_id,
        "Rating:",
        rating.rating,
    )


# =============================
# TEST 3: MOVIE RATINGS
# =============================  

ratings = get_movie_ratings(1)

print("\nToy Story Ratings:")
print("Total ratings:", len(ratings))


# =============================
# TEST 4: AVERAGE RATING
# =============================

average = get_movie_average_rating(1)

print("\nToy Story Average Rating:")
print(average)


# =============================
# TEST 5: MOST RATED MOVIES
# =============================

movies = get_most_rated_movies(10)

print("\nTop 10 Most Rated Movies:")

for movie in movies:
    print(
        movie["movie_id"],
        movie["title"],
        movie["rating_count"],
    )

# =============================
# TEST 6: USER RATINGS WITH MOVIES
# =============================

user_ratings = get_user_ratings_with_movies(1)

print("\nUser 1 Ratings with Movie names:")

for row in user_ratings[:5]:
    print(
        "User ID:", row.user_id,
        "Movie ID:", row.movie_id,
        "Rating:", row.rating,
        "Movie Title:", row.title
    )


# =============================
# TEST 7: ALL RATINGS
# =============================

print("\nTEST 7 STARTED")

all_ratings = get_all_ratings_for_recommendation()

print("\nAll Ratings for Recommendation:")
print("Total ratings:", len(all_ratings))

for row in all_ratings[:5]:
    print(
        "User ID:", row.user_id,
        "Movie ID:", row.movie_id,
        "Rating:", row.rating,
    )