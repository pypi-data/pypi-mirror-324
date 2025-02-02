import numpy as np


#sigmoid function to get the probability betweeen [0 , 1]
def sigmoid(z):
    return 1/(1 + np.exp(-z))


class LogisticRegression():
    #attributes to build the model
    def __init__(self, lr = 0.001, iterations = 1000):
        self.lr = lr
        self.interations = iterations
        self.weights = None
        self.bias = 0
    

    """
        training function, where weights and bias are adjusts iteratively 
    """
    def learn(self, X, y):
        n_samples, n_features = X.shape
        self.weights = np.zeros(n_features)
        
        for _ in range(self.interations):
            linear_model_pred = np.dot(X, self.weights) + self.bias
            prediction = sigmoid(linear_model_pred)
            
            #gradient values 
            dw = (1/n_samples) * np.dot(X.T, (prediction - y))
            db = (1/n_samples) * np.sum(prediction - y)
            
            #adjusting the weight and bias accorfing to the gradient values
            self.weights = self.weights - self.lr*dw
            self.bias = self.bias - self.lr*db
       
     
        
    """ this is a predicting function"""
    def predict(self, X):
         linear_model_pred = np.dot(X, self.weights) + self.bias
         y_pred = sigmoid(linear_model_pred)
         
         pred = [0 if y<=0.5 else 1 for y in y_pred]
         
         return np.array(pred)