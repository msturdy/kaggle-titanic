#!/usr/bin/python3

import pickle

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier

# This imports the prepareData.py file from our "bin" folder
# from bin import prepareData
from bin import helperFunctions

# print out more information
print_debug = 1

pickled_datasets_file = 'data/pickled_datasets.bin'
submission_file = 'submission.csv'

x_train, y_train, x_test = pickle.load(open(pickled_datasets_file, 'rb'))

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
