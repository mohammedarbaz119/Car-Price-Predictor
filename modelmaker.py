import numpy as np
import pandas as pd
import json
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import scale
from sklearn.model_selection import train_test_split
from sklearn import metrics
import pickle

dataset = pd.read_csv('./CarPrice_Assignment.csv')

X = dataset.drop(['price'], axis=1)
X = X.drop(['car_ID'], axis=1)
X['Car_Company'] = X['CarName'].apply(lambda x: x.split(" ")[0])
car_companies = set([i for i in X['Car_Company']])
X = X.drop(['CarName'], axis=1)
categorical_set = X.select_dtypes(include=['object'])
dummies = pd.get_dummies(categorical_set)
X = X.drop([*categorical_set], axis=1)
X = pd.concat([X, dummies], axis=1)


y = dataset['price']

Xt, Xtest, yt, ytest = train_test_split(X, y, test_size=0.2, random_state=65)
lr = LinearRegression()
lr.fit(Xt, yt)
pickle.dump(lr, open('LinearRegression.pkl', 'wb'))
print(ytest)

c = lr.predict(Xtest)
print(f"error is {metrics.r2_score(ytest,c)}")
d = lr.predict([Xtest.iloc[1]])
print(d)
