import numpy as np
from collections import Counter



class knn:
    def __init__(self, k=3):
        """
        Initialize the KNN classifier.

        """
        self.k = k

    def fit(self, X, y):
        """
        Fit the model using the training data.

        """
        self.X_train = np.array(X)
        self.y_train = np.array(y)

    def euclidean_distance(self, x1, x2):
        """
        Calculate the Euclidean distance between two points.

        """
        return np.sqrt(np.sum((x1 - x2) ** 2))

    def predict(self, X):
        """
        Predict the labels for the given test data.

        """
        X = np.array(X)
        predictions = [self.helper_predict(x) for x in X]
        return predictions

    def helper_predict(self, x):
        """
        Predict the label for a single instance.

        """
        # Calculate distances between x and all training points
        distances = [self.euclidean_distance(x, x_train) for x_train in self.X_train]

        # Get the indices of the k-nearest neighbors
        k_indices = np.argsort(distances)[:self.k]

        # Get the labels of the k-nearest neighbors
        k_nearest_labels = [self.y_train[i] for i in k_indices]

        # Return the most common label among the k-nearest neighbors
        most_common = Counter(k_nearest_labels).most_common(1)[0][0]
        return most_common
