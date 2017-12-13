## Useful functions for preparing data
##
import sys
import pickle
from sklearn.model_selection import GridSearchCV
from bin.exceptions import PickleFileException

##  report the best parameters that have been tried for given model, param_grid and data
##  then return the tuned model
def getTunedModel(model, param_grid, x_train, y_train):
    print("Calculating best params for model from: {}".format(param_grid))
    
    CV_model = GridSearchCV(estimator=model, param_grid=param_grid, cv=5)
    CV_model.fit(x_train, y_train)

    print("Found best parameters '{}'".format(CV_model.best_params_))
    
    # return CV_model.best_params_
    return CV_model


##  take python objects and write to disk, to be picked up later
def storePickledData(data, filename):
    
    try:
        pickled_data_file = open(filename, 'wb')

    except IOError as e:
        print('ERROR: opening file {}: {}'.format(filename, e))
        sys.exit(1)
    
    else:
        pickle.dump(data, pickled_data_file)
        pickled_data_file.close()
        print('Datasets pickled into {}'.format(filename))


##  read a pickled file from disk and return the contents.
def loadPickledData(filename):
    
    try:
        pickled_data_file = open(filename, 'rb')

    except FileNotFoundError:
        raise PickleFileException("No file found at {}".format(filename))
 
    except IOError as e:
        raise PickleFileException("ERROR accessing file at {}: {}".format(filename, e))
        
    else:
        pickled_data = pickle.load(pickled_data_file)
        pickled_data_file.close()
        
        return pickled_data
