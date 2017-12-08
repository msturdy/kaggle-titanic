#!/usr/bin/python3

import sys
import pickle

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier

# from bin import prepareData
from bin.helperFunctions import loadPickledData, getBestParametersUsingGridSearch
from bin.exceptions import NoPickleFileException


# print out more information
print_debug = 1

pickled_datasets_file = 'data/pickled_datasets.bin'
submission_file = 'submission.csv'

# needed for displaying in wide console without wrapping text
pd.set_option('display.max_colwidth', 30)
pd.set_option('expand_frame_repr', False)

try:
    x_train, y_train, x_test, test = loadPickledData(pickled_datasets_file)
except NoPickleFileException:
    print('File not found at {}'.format(pickled_datasets_file))
    sys.exit(1) 


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

best_params_random_forest = getBestParametersUsingGridSearch(model, param_grid, x_train, y_train)

print("Found best parameters: {}".format(best_params_random_forest))

model.fit(x_train, y_train)
print('\nAccuracy from training dataSet: {}%'.format(round(model.score(x_train, y_train) * 100, 2)))

y_pred = model.predict(x_test)

submission = pd.DataFrame({
   "PassengerId": test["PassengerId"],
   "Survived": y_pred
})

submission.to_csv(submission_file, index=False)
print('Submission data written to [{}]'.format(submission_file))