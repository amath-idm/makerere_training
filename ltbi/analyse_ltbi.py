"""
Set up classifers for analysing LTBI data
"""

# Imports
from sklearn.linear_model import LogisticRegression
import pandas as pd

# Read in the data and make a plot
ltbi = pd.read_csv("ltbi_data.csv")

# Create testing and training data
n_train = 300  # Use this many points to train the model
x_train = ltbi[['bar_hours', 'school_hours']].to_numpy()[:n_train]
y_train = ltbi['infected'].to_numpy()[:n_train]
x_test = ltbi[['bar_hours', 'school_hours']].to_numpy()[n_train:]
y_test = ltbi['infected'].to_numpy()[n_train:]

### Make classifers

# Logistic regression
lr = LogisticRegression(max_iter=1000)
lr.fit(x_train, y_train)
print("score on test: " + str(lr.score(x_test, y_test)))
print("score on train: " + str(lr.score(x_train, y_train)))

# Naive Bayes
from sklearn.naive_bayes import MultinomialNB
mnb = MultinomialNB().fit(x_train, y_train)
print("score on test: " + str(mnb.score(x_test, y_test)))
print("score on train: "+ str(mnb.score(x_train, y_train)))

# Add others as needed
