#!/usr/bin/python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier

# This imports the prepareData.py file from our "bin" folder
from bin import prepareData
from bin import helperFunctions

# print out more information
print_debug = 1

train_file_in   = 'data/train.csv'
test_file_in    = 'data/test.csv'
submission_file = 'submission.csv'

pd.set_option('display.max_colwidth', 30)
pd.set_option('expand_frame_repr', False)

train = pd.read_csv(train_file_in)
test  = pd.read_csv(test_file_in)
dataSets = [train, test]

# prepareData contains all the functions for adding features to the datasets
dataSets = prepareData.prepare(dataSets)

if print_debug:
    print('\n', train.describe())
    print("\n", train[['Gender', 'Survived']].groupby('Gender', as_index=False).mean())
    print("\n", train[['AgeGroup', 'Survived']].groupby('AgeGroup', as_index=False).mean())
    print("\n", train[['Deck', 'Survived']].groupby('Deck', as_index=False).mean())
    print("\n", train[['FamilySize', 'Survived']].groupby('FamilySize', as_index=False).mean())
    print("\n", train[['Port', 'Survived']].groupby('Port', as_index=False).mean())
    print("\n", train[['Title', 'Survived']].groupby('Title', as_index=False).mean())
    print("\n", train[['Class', 'Survived']].groupby('Class', as_index=False).mean())

## drop unneeded features
if print_debug:
    print('Before trimming unneeded features:\n', train.head(1))

for feature in ['Pclass', 'Name', 'Sex', 'Age', 'Ticket', 'Fare', 'Cabin', 'Embarked']:
        train = train.drop(feature, axis=1)
        test  = test.drop(feature, axis=1)

# needed in test DS to generate the submission file.
train = train.drop('PassengerId', axis=1)

if print_debug:
    print('\nAfter trimming unneeded features:\n', train.head(1))

# prepare data sets for the model(s)
x_train = train.drop('Survived', axis=1)
y_train = train['Survived']
x_test  = test.drop('PassengerId', axis=1).copy()

if print_debug:
    print("\n\ndataSets shapes:", x_train.shape, y_train.shape, x_test.shape)
    print("x_train.head()\n", x_train.head())
    print("x_test.head()\n", x_test.head())


model  = RandomForestClassifier(n_jobs=2)
# the parameter grid to search across
param_grid = {
    "max_depth": [5,10],
    "n_estimators": [100,1000]
}

print("\nCalculating best params for the RandomForestClassifier...")
best_params_random_forest = helperFunctions.getBestParametersUsingGridSearch(model, param_grid, x_train, y_train)

print("Found best parameters: {}".format(best_params_random_forest))

#model.fit(x_train, y_train)
#y_pred = model.predict(x_test)

#print('\nAccuracy from training dataSet: {}%'.format(round(model.score(x_train, y_train) * 100, 2)))

#submission = pd.DataFrame({
#    "PassengerId": test["PassengerId"],
#    "Survived": y_pred
#})

#submission.to_csv(submission_file, index=False)
#print('Submission data written to [{}]'.format(submission_file))
