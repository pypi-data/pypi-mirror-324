import numpy as np
from sklearn.utils import resample
from modelml.Decision_Tree import DecisionTree

# Class implementing a Random Forest
class RandomForest:
    def __init__(self, n_estimators=10, max_depth=None, max_features=None):
        # Number of trees in the forest
        self.n_estimators = n_estimators
        # Maximum depth of each tree
        self.max_depth = max_depth
        # Maximum number of features to consider for splitting
        self.max_features = max_features
        # List to hold the individual decision trees
        self.trees = []

    def fit(self, X, y):
        self.trees = []  # Reset trees for a fresh training
        for _ in range(self.n_estimators):
            # Bootstrap sampling to create subsets of the data
            X_sample, y_sample = resample(X, y, random_state=np.random.randint(1000))
            
            # Initialize and train a decision tree
            tree = DecisionTree(max_depth=self.max_depth)
            tree.fit(X_sample, y_sample)
            self.trees.append(tree)

    def predict(self, X):
        # Collect predictions from all trees
        tree_predictions = np.array([tree.predict(X) for tree in self.trees])
        # Perform majority voting
        majority_votes = np.apply_along_axis(lambda x: np.bincount(x).argmax(), axis=0, arr=tree_predictions)
        return majority_votes
