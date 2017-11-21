
from sklearn.grid_search import GridSearchCV

#  report the best parameters that have been tried for given model, param_grid and data
def getBestParametersUsingGridSearch(model, param_grid, x_train, y_train):
    CV_model = GridSearchCV(estimator=model, param_grid=param_grid, cv=5)
    CV_model.fit(x_train, y_train)
    
    return CV_model.best_params_
