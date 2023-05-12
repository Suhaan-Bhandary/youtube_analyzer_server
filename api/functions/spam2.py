import pandas as pd
import string
import re
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
import os
from django.conf import settings



# Load the dataset
csv_path = os.path.join(settings.STATIC_ROOT, 'Youtube01.csv')
data = pd.read_csv(csv_path, encoding='latin1')


# Preprocess the text data
stop_words = set(stopwords.words('english') + list(string.punctuation))
lemmatizer = nltk.stem.WordNetLemmatizer()

def preprocess(text):
    text = text.lower()
    text = re.sub('<[^>]+>', '', text)
    text = re.sub('\d+', '', text)
    words = nltk.word_tokenize(text)
    words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]
    return ' '.join(words)

data['Comment'] = data['Comment'].apply(preprocess)

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(data['Comment'], data['Spam'], test_size=0.2)

# Create a pipeline to vectorize and train the data
pipeline = Pipeline([
    ('vectorizer', CountVectorizer()),
    ('classifier', MultinomialNB())
])

# Train the model
model = pipeline.fit(X_train, y_train)

# Test the model on new data
def is_spam(text):
    text = preprocess(text)
    return model.predict([text])[0] == 1


text = "congrats  vishal  "
#congratualtion vishal u won a lottery 
#vishal plays football

print(is_spam(text)) # Returns True
