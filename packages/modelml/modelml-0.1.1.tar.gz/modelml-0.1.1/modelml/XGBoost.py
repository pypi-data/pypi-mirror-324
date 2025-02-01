import numpy as np
from sklearn.metrics import mean_squared_error
class Node:
    def __init__(self, feature=None, threshold=None, left=None, right=None, value=None):
        self.feature = feature
        self.threshold = threshold
        self.left = left
        self.right = right
        self.value = value

# Optimized decision tree implementation for regression

class DecisionTreeRegression:
    def __init__(self, max_depth=None):
        self.max_depth = max_depth
        self.root = None

    def fit(self, X, y):
        self.root = self._build_tree(X, y)

    def predict(self, X):
        return np.array([self._traverse_tree(x, self.root) for x in X])

    def _build_tree(self, X, y, depth=0):
        num_samples, num_features = X.shape
        if depth >= self.max_depth or num_samples < 2:
            leaf_value = np.mean(y)
            return Node(value=leaf_value)
        
        best_feature, best_threshold = self._best_split(X, y)
        if best_feature is None:
            leaf_value = np.mean(y)
            return Node(value=leaf_value)
        
        left_indices = X[:, best_feature] <= best_threshold
        right_indices = X[:, best_feature] > best_threshold
        
        left_child = self._build_tree(X[left_indices], y[left_indices], depth + 1)
        right_child = self._build_tree(X[right_indices], y[right_indices], depth + 1)
        return Node(feature=best_feature, threshold=best_threshold, left=left_child, right=right_child)

    def _best_split(self, X, y):
        num_samples, num_features = X.shape
        best_mse = float('inf')
        best_feature, best_threshold = None, None
        
        for feature in range(num_features):
            thresholds = np.unique(X[:, feature])

            # Try a subset of thresholds for speed
            
            if len(thresholds) > 10:
                thresholds = np.linspace(thresholds.min(), thresholds.max(), 10)
            for threshold in thresholds:
                mse = self._mean_squared_error(X, y, feature, threshold)
                if mse < best_mse:
                    best_mse = mse
                    best_feature = feature
                    best_threshold = threshold
        
        return best_feature, best_threshold

    def _mean_squared_error(self, X, y, feature, threshold):
        left_indices = X[:, feature] <= threshold
        right_indices = X[:, feature] > threshold
        
        if len(y[left_indices]) == 0 or len(y[right_indices]) == 0:
            return float('inf')
        
        mse_left = np.mean((y[left_indices] - np.mean(y[left_indices])) ** 2)
        mse_right = np.mean((y[right_indices] - np.mean(y[right_indices])) ** 2)
        mse = (len(y[left_indices]) * mse_left + len(y[right_indices]) * mse_right) / len(y)
        return mse

    def _traverse_tree(self, x, node):
        if node.value is not None:
            return node.value
        
        if x[node.feature] <= node.threshold:
            return self._traverse_tree(x, node.left)
        return self._traverse_tree(x, node.right)

class xgBoost:
    def __init__(self, n_estimators=100, learning_rate=0.001, max_depth=3):
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.max_depth = max_depth
        self.trees = []

    def _gradient(self, y_true, y_pred):
        return y_true - y_pred  # Gradient for regression is the residual error

    def fit(self, X, y):
        n_samples = X.shape[0]
        y_pred = np.zeros(n_samples)  # Initialize prediction as zeros

        print("\n For training dataset: ")
        for i in range(self.n_estimators):
            gradient = self._gradient(y, y_pred)
            
            # Use the optimized custom decision tree
            tree = DecisionTreeRegression(max_depth=self.max_depth)
            tree.fit(X, gradient)  # Fit tree on the residuals
            update = tree.predict(X)
            
            y_pred += self.learning_rate * update  # Update the prediction
            


    def predict(self, X):
        y_pred = np.zeros(X.shape[0])
        for tree in self.trees:
            y_pred += self.learning_rate * tree.predict(X)  # No rounding for regression
        return y_pred  # Return continuous output
    

