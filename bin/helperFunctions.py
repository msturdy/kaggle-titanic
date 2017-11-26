
import pickle
from sklearn.grid_search import GridSearchCV
from bin.exceptions import NoPickleFileException

#  report the best parameters that have been tried for given model, param_grid and data
def getBestParametersUsingGridSearch(model, param_grid, x_train, y_train):
    CV_model = GridSearchCV(estimator=model, param_grid=param_grid, cv=5)
    CV_model.fit(x_train, y_train)
    
    return CV_model.best_params_


# take python objects and write to disk, to be picked up later
def storePickledData(data, filename):
    
    with open(filename, 'wb') as pickled_data_file:
        pickle.dump(data, pickled_data_file)

    return True


# read a pickled file from disk and return the contents.
def loadPickledData(filename):
    
    try:
        with open(filename, 'rb') as pickled_data_file:
            return pickle.load(pickled_data_file)

    except FileNotFoundError:
        raise NoPickleFileException("No file found at {}".format(filename))
 
