import numpy as np
from tqdm import tqdm 


class My_SVM():
    def __init__(self, learning_rate=0.01, lambda_param=0.5, epochs=100):
        self.lr = learning_rate
        self.lambda_param = lambda_param
        self.epochs = epochs
        self.w = None
        self.b = None
        self.cost_history = []
        
    def cost_function(self, X, y):
        
        predictions = np.dot(X, self.w) + self.b
        # hinge loss calculation
        losses = np.maximum(0, 1 - y * predictions)

        # Add regularization (1/2|`w`|^2)
        return np.mean(losses) + self.lambda_param * np.dot(self.w, self.w)
    
    def fit(self, X, y):
        n_samples, n_features = X.shape
        
        # Convert labels to -1 and 1
        y = np.where(y <= 0, -1, 1)
        
        # Initialize parameters
        self.w = np.zeros(n_features)
        self.b = 0
        
        # Gradient descent
        for _ in tqdm(range(self.epochs)):
            # Make predictions   w.x+b
            predictions = np.dot(X, self.w) + self.b
            
            # Calculate condition y(w.x+b)
            
            condition = y * predictions >= 1   #greater than 1 -> correctly classified and outside margin
                #else misclassified or inside margin
            
            # Gradient calculation for weights
            dw = 2 * self.lambda_param * self.w

            
            mask = ~condition   #misclassified or inside margin
            if np.any(mask):    #if any sample is misclassified or inside margin
                dw -= np.dot(X[mask].T, y[mask]) / n_samples
            
            # Gradient calculation for bias
            if np.any(mask):
                db = -np.mean(y[mask]) 
            else:
                db = 0
            
            # Update parameters
            self.w -= self.lr * dw
            self.b -= self.lr * db
            
            
            cost = self.cost_function(X, y)
            self.cost_history.append(cost)
    
    def predict(self, X):
        predictions = np.dot(X, self.w) + self.b
        return np.where(predictions <= 0, 0, 1)