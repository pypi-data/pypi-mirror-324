import numpy as np


class MultipleLinearRegression:
    def __init__(self, learning_rate=0.01, epochs=1000):
        self.learning_rate = learning_rate  # Learning rate
        self.epochs = epochs  # Number of iterations
        self.weights = None  # Initialize weights
        self.bias = None  # Initialize bias

    # Linear model prediction
    def predict(self, X):
        return np.dot(X, self.weights) + self.bias

    # Mean Squared Error (MSE) Loss function
    def compute_loss(self, X, y):
        m = len(y)
        predictions = self.predict(X)
        loss = (1 / (2 * m)) * np.sum((predictions - y) ** 2)
        return loss

    # Training the model using gradient descent
    def fit(self, X, y):
        m = len(y)
        n = X.shape[1]  # Number of features
        self.weights = np.zeros(n)  # Initialize weights
        self.bias = 0  # Initialize bias
        
        # Gradient Descent loop
        for epoch in range(self.epochs):
            predictions = self.predict(X)
            
            # Gradients for weights and bias
            dw = (1 / m) * np.dot(X.T, (predictions - y))
            db = (1 / m) * np.sum(predictions - y)
            
            # Update weights and bias
            self.weights -= self.learning_rate * dw
            self.bias -= self.learning_rate * db
            

