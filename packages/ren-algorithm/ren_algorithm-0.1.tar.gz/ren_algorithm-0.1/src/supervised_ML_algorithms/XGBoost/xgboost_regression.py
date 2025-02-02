import numpy as np

from decision_tree import DecisionTreeRegressor


class CustomXGBoostRegressor:
    #attributes to build XGBoostRegressor
    def __init__(self, n_estimators=100, learning_rate=0.1, max_depth=3):
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.max_depth = max_depth
        self.models = []

    
    #learning
    def fit(self, X, y):
        y_pred = np.mean(y) 
        self.initial_prediction = y_pred
        
        #gradient boosting: minimizes the residuals sequentially
        for _ in range(self.n_estimators):
            residual = y - y_pred
            tree = DecisionTreeRegressor(max_depth=self.max_depth)
            
            tree.fit(X, residual)
            
            tree_pred = tree.predict(X)
            y_pred += self.learning_rate * tree_pred
            self.models.append(tree)


    #prediction function
    def predict(self, X):
        
        predictions = np.full(X.shape[0], self.initial_prediction)
        for tree in self.models:
            predictions += self.learning_rate * tree.predict(X)
        return predictions