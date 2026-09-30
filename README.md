# Movie Recommendation System

A movie recommendation system built using Python, PostgreSQL, SQLAlchemy ORM, FastAPI, and Streamlit.

## Project Overview

This project recommends movies based on user preferences and movie similarity.

The system uses collaborative filtering techniques to generate recommendations.

## Features

- User-based movie recommendations
- Item-based similar movie recommendations
- Movie rating dashboard
- Most rated movies
- Highest rated movies
- Rating distribution
- Total users, movies, and ratings
- PostgreSQL database
- SQLAlchemy ORM
- FastAPI REST API
- Streamlit web interface

## Technology Stack

- Python
- Pandas
- NumPy
- Scikit-learn
- PostgreSQL
- SQLAlchemy
- FastAPI
- Streamlit
- Matplotlib
- Seaborn

## Project Structure

```text
Movie-Recommendation-System/
│
├── api/
│   └── main.py
│
├── Data_layer/
│   ├── movies.csv
│   ├── ratings.csv
│   ├── links.csv
│   └── data_loader.py
│
├── Database/
│   ├── database.py
│   ├── models.py
│   ├── queries.py
│   ├── create_tables.py
│   ├── load_data.py
│   └── load_links.py
│
├── Model_layer/
│   ├── user_based.py
│   ├── item_based.py
│   └── content_based.py
│
├── Preprocessing_layer/
│   └── preprocessing.py
│
├── UI_layer/
│   └── streamlit_app.py
│
├── requirements.txt
├── test_queries.py
├── test_user_based.py
└── .gitignore