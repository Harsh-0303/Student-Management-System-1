import streamlit as st
import requests
import pandas as pd

from Database.queries import (
    get_total_ratings,
    get_total_users,
    get_total_movies,
    get_average_rating,
    get_most_rated_movies,
    get_rating_distribution,
    get_highest_rated_movies,
    get_all_movies_for_recommendation
)


# =========================================
# PAGE CONFIGURATION
# =========================================

st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="wide"
)


# =========================================
# CUSTOM CSS
# =========================================

st.markdown(
    """
<style>

.main {
    background-color: #0e1117;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}

.hero {
    padding: 30px;
    border-radius: 15px;
    background: linear-gradient(
        135deg,
        #111827,
        #1f2937
    );
    border: 1px solid #374151;
    margin-bottom: 30px;
}

.hero-title {
    font-size: 42px;
    font-weight: 700;
    margin-bottom: 8px;
}

.hero-subtitle {
    font-size: 17px;
    color: #9ca3af;
}

.section-title {
    font-size: 26px;
    font-weight: 600;
    margin-top: 20px;
    margin-bottom: 15px;
}

.metric-card {
    background-color: #1f2937;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #374151;
    text-align: center;
}

.metric-title {
    color: #9ca3af;
    font-size: 14px;
}

.metric-value {
    font-size: 28px;
    font-weight: 700;
    margin-top: 5px;
}

.recommendation-box {
    background-color: #111827;
    padding: 25px;
    border-radius: 15px;
    border: 1px solid #374151;
    margin-top: 10px;
    margin-bottom: 20px;
}

</style>
""",
    unsafe_allow_html=True
)


# =========================================
# HERO SECTION
# =========================================

st.markdown(
    """
<div class="hero">
    <div class="hero-title">
        🎬 Movie Recommendation System
    </div>
    <div class="hero-subtitle">
        Discover movies, explore ratings, and get
        personalized recommendations powered by
        collaborative filtering.
    </div>
</div>
""",
    unsafe_allow_html=True
)


# =========================================
# DASHBOARD DATA
# =========================================

total_ratings = get_total_ratings()
total_users = get_total_users()
total_movies = get_total_movies()
average_rating = get_average_rating()


# =========================================
# DASHBOARD CARDS
# =========================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.markdown(
        f"""
<div class="metric-card">
    <div class="metric-title">
        Total Ratings
    </div>
    <div class="metric-value">
        {total_ratings:,}
    </div>
</div>
""",
        unsafe_allow_html=True
    )


with col2:

    st.markdown(
        f"""
<div class="metric-card">
    <div class="metric-title">
        Total Users
    </div>
    <div class="metric-value">
        {total_users:,}
    </div>
</div>
""",
        unsafe_allow_html=True
    )


with col3:

    st.markdown(
        f"""
<div class="metric-card">
    <div class="metric-title">
        Total Movies
    </div>
    <div class="metric-value">
        {total_movies:,}
    </div>
</div>
""",
        unsafe_allow_html=True
    )


with col4:

    st.markdown(
        f"""
<div class="metric-card">
    <div class="metric-title">
        Average Rating
    </div>
    <div class="metric-value">
        ⭐ {average_rating:.2f}
    </div>
</div>
""",
        unsafe_allow_html=True
    )


st.divider()


# =========================================
# MOVIE INSIGHTS
# =========================================

st.markdown(
    """
<div class="section-title">
    🍿 Movie Insights
</div>
""",
    unsafe_allow_html=True
)


col1, col2 = st.columns(2)


# =========================================
# MOST RATED MOVIES
# =========================================

with col1:

    st.markdown("### 🍿 Most Rated Movies")

    most_rated_movies = get_most_rated_movies(
        limit=10
    )

    st.dataframe(
        most_rated_movies,
        use_container_width=True,
        hide_index=True
    )


# =========================================
# HIGHEST RATED MOVIES
# =========================================

with col2:

    st.markdown("### ⭐ Highest Rated Movies")

    highest_rated_movies = get_highest_rated_movies(
        limit=10
    )

    st.dataframe(
        highest_rated_movies,
        use_container_width=True,
        hide_index=True
    )


st.divider()


# =========================================
# RATING DISTRIBUTION
# =========================================

st.markdown(
    """
<div class="section-title">
    📊 Rating Distribution
</div>
""",
    unsafe_allow_html=True
)


rating_distribution = get_rating_distribution()


st.bar_chart(
    rating_distribution,
    use_container_width=True
)


st.divider()


# =========================================
# PERSONALIZED RECOMMENDATIONS
# =========================================

st.markdown(
    """
<div class="section-title">
    🎯 Personalized Recommendations
</div>
""",
    unsafe_allow_html=True
)


st.markdown(
    '<div class="recommendation-box">',
    unsafe_allow_html=True
)


user_id = st.number_input(
    "Enter User ID",
    min_value=1,
    step=1
)


if st.button(
    "🎯 Get Recommendations",
    use_container_width=True
):

    url = (
        f"http://127.0.0.1:8000/"
        f"recommendations/user/{user_id}"
    )

    try:

        response = requests.get(url)

        if response.status_code == 200:

            recommendations = response.json()

            st.success(
                f"Recommendations generated for User {user_id}"
            )

            st.dataframe(
                recommendations,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.error(
                f"Could not get recommendations. "
                f"Status Code: {response.status_code}"
            )

    except requests.exceptions.ConnectionError:

        st.error(
            "Could not connect to FastAPI server. "
            "Please make sure FastAPI is running."
        )


st.markdown(
    "</div>",
    unsafe_allow_html=True
)


# =========================================
# SIMILAR MOVIES
# =========================================

st.markdown(
    """
<div class="section-title">
    🎥 Explore Similar Movies
</div>
""",
    unsafe_allow_html=True
)


st.markdown(
    '<div class="recommendation-box">',
    unsafe_allow_html=True
)


# =========================================
# LOAD MOVIES
# =========================================

movie_data = get_all_movies_for_recommendation()


movies_df = pd.DataFrame(
    movie_data,
    columns=["movieId", "title"]
)


# =========================================
# MOVIE SELECTION
# =========================================

selected_movie = st.selectbox(
    "Select a Movie",
    movies_df["title"].tolist()
)


selected_movie_id = int(
    movies_df[
        movies_df["title"] == selected_movie
    ]["movieId"].iloc[0]
)


st.write(
    f"**Movie ID:** {selected_movie_id}"
)


# =========================================
# FIND SIMILAR MOVIES
# =========================================

if st.button(
    "🎥 Find Similar Movies",
    use_container_width=True
):

    url = (
        f"http://127.0.0.1:8000/"
        f"recommendations/movie/{selected_movie_id}"
    )

    try:

        response = requests.get(url)

        if response.status_code == 200:

            similar_movies = response.json()

            st.success(
                f"Movies similar to {selected_movie}"
            )

            st.dataframe(
                similar_movies,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.error(
                f"Could not find similar movies. "
                f"Status Code: {response.status_code}"
            )

    except requests.exceptions.ConnectionError:

        st.error(
            "Could not connect to FastAPI server. "
            "Please make sure FastAPI is running."
        )


st.markdown(
    "</div>",
    unsafe_allow_html=True
)


# =========================================
# FOOTER
# =========================================

st.divider()


st.markdown(
    """
<div style="text-align:center; color:#6b7280;">
    🎬 Movie Recommendation System
    <br>
    Powered by Python • PostgreSQL • SQLAlchemy • FastAPI • Streamlit
</div>
""",
    unsafe_allow_html=True
)