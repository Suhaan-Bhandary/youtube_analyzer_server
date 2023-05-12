import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import BernoulliNB
import os
from django.conf import settings

def isTextSpam(text):
    csv_path = os.path.join(settings.STATIC_ROOT, 'Youtube01.csv')
    data = pd.read_csv(csv_path)
    # print(data.sample(5)) #This will print 5 random rows from the dataset

    # print(data.isnull().sum())

    # Since we only require content and class columns, we will update our existing datafram to the following
    data = data[['CONTENT', 'CLASS']]

    # We will map 0 to not spam and 1 to span in class column
    data["CLASS"] = data['CLASS'].map({0: "not spam", 1: "spam"})
    # print(data.sample(5))

    x = np.array(data['CONTENT'])
    y = np.array(data['CLASS'])

    """
    As the output of this problem will either be 0 or 1,i.e, the problem of binary classification,
    we can use the Bernoulli Naive Bayes algorithm to train the model:
    """

    cv = CountVectorizer(stop_words='english')
    x = cv.fit_transform(x)
    xtrain, xtest, ytrain, ytest = train_test_split(
        x, y, train_size=0.8, random_state=42)

    model = BernoulliNB()
    model.fit(xtrain, ytrain)

    # Its time to check the model by giving spam and non-spam comments
    d = cv.transform([text]).toarray()

    return model.predict(d)[0] == "spam"
