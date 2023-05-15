import os
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.conf import settings
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB


def getMovieRecommendations(user_input_title, user_input_genre):
    csv_path = os.path.join(settings.STATIC_ROOT, 'netflix_titles.csv')

    # Load the Netflix movie dataset from a CSV file
    netflix_data = pd.read_csv(csv_path)

    # Convert the text data into numerical features
    vectorizer = CountVectorizer(stop_words='english')
    X = vectorizer.fit_transform(netflix_data['description'])
    y = netflix_data['listed_in']

    # Train a Multinomial Naive Bayes classifier on all the data
    clf = MultinomialNB()
    clf.fit(X, y)

    # Convert the input genre into numerical features
    X_input = vectorizer.transform([user_input_genre])

    # Predict the genre of the movie using the classifier
    predicted_genre = clf.predict(X_input)

    # Filter the Netflix movie dataset by predicted genre
    genre_data = netflix_data[netflix_data['listed_in'] == predicted_genre[0]]

    # Print the titles of movies in the filtered dataset
    # print("Matching movies:")
    # for title in genre_data['title']:
    #     print(title)

    movies = []
    for idx in range(5):
        movies.append({
            "date" : genre_data.iloc[idx]["release_year"],
            "title" : genre_data.iloc[idx]["title"],
            "description" : genre_data.iloc[idx]["description"]
        })
        
    return movies
