import os
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.conf import settings
import numpy as np

def getMovieRecommendations(user_input_title, user_input_genre):
    # Load the Netflix dataset
    csv_path = os.path.join(settings.STATIC_ROOT, 'netflix_titles.csv')
    netflix_data = pd.read_csv(csv_path)

    # Preprocess the dataset
    netflix_data["listed_in"] = netflix_data["listed_in"].apply(lambda x: [i.strip() for i in x.split(",")])
    netflix_data["description"] = netflix_data["description"].apply(lambda x: x.lower())

    # Create a CountVectorizer to convert text into vectors
    vectorizer = CountVectorizer(stop_words="english")

    # Create a sparse matrix of the movie descriptions
    movie_descriptions = vectorizer.fit_transform(netflix_data["description"])

    # Compute the cosine similarity matrix of the movie descriptions
    cosine_sim_matrix = cosine_similarity(movie_descriptions)

    # Get user input for movie title and genre
    user_input_title = input("Enter movie title: ")
    user_input_genre = input("Enter movie genre: ")

    # Find the indices of movies with the given genre
    genre_indices = netflix_data[netflix_data["listed_in"].apply(lambda x: user_input_genre.lower() in [i.lower() for i in x])].index

    # Find the indices of movies with the given title
    title_indices = netflix_data[netflix_data["title"].apply(lambda x: user_input_title.lower() in x.lower())].index

    # Find the intersection of the two sets of indices
    movie_indices = list(set(genre_indices).intersection(set(title_indices)))

    # Convert the user input into a vector
    user_input_vector = vectorizer.transform([user_input_title + ' ' + user_input_genre])

    # Find the top 5 most similar movies
    similarity_scores = list(enumerate(cosine_sim_matrix[user_input_vector[0].toarray()[0]]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1][0], reverse=True)
    top_5_movie_indices = [i[0] for i in similarity_scores[1:6]]

    # Print the top 5 movies
    print("Top 5 similar movies to {} in the genre of {}: ".format(user_input_title, user_input_genre))

    movies = []
    for idx in top_5_movie_indices:
        movies.append({
            "date" : netflix_data.iloc[idx]["release_year"],
            "title" : netflix_data.iloc[idx]["title"],
            "description" : netflix_data.iloc[idx]["description"]
        })
        
    return movies