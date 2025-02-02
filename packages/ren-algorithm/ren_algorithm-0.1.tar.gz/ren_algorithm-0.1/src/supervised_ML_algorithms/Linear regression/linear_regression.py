import numpy as np


class LinearRegression():
    #attributes required to build the model
    def __init__(self, lr = 0.01, iterations = 1000):
        self.lr = lr
        self.iterations = iterations
        self.weight = None
        self.bias = 0
    
    
    #actually learn/fitting model
    def learn(self, X, y):
        samples, features = X.shape
        self.weight = np.zeros(features)
        
        for _ in range(self.iterations):
            
            y_pred = np.dot(X, self.weight) + self.bias
            
            #gradients
            dw = (1/samples) * np.dot(X.T, (y_pred- y))
            db = (1/samples) * np.sum(y_pred - y)
            
            #adjusting weight and bias
            self.weight = self.weight - self.lr * dw
            self.bias = self.bias - self.lr * db
            
     
     #predicting function   
    def predict(self, X):
        y_pred = np.dot(X, self.weight) + self.bias
        return y_pred
