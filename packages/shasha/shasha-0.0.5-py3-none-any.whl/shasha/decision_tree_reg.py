import numpy as np
from collections import Counter


class Node:
    def __init__(
        self, feature=None, threshold=None, left=None, right=None, *, value=None
   ,var=None ):
        self.feature = feature
        self.threshold = threshold
        self.left = left
        self.right = right
        self.value = value

    def is_leaf_node(self):
        return self.value is not None
 

class My_DecisionTree_Regressor:
    def __init__(self, max_depth=None, min_samples_split=2):
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.root = None

    def fit(self, X, y):
        self.n_classes = 1  # For regression
        self.root = self._grow_tree(X, y)

    def _grow_tree(self, X, y, depth=0):
        n_samples, n_features = X.shape
        
        # Check stopping criteria
        if (self.max_depth is not None and depth >= self.max_depth) or (n_samples < self.min_samples_split):
            leaf_value = np.mean(y)
            return Node(value=leaf_value)

        # Find the best split
        best_feature = None
        best_threshold = None
        best_var_reduction = -float("inf")
        parent_var = np.var(y)

        for feature_idx in range(n_features):
            feature_values = X[:, feature_idx]
            thresholds = np.unique(feature_values)
            
            for threshold in thresholds:
                left_mask = feature_values <= threshold
                right_mask = ~left_mask
                
                if np.sum(left_mask) == 0 or np.sum(right_mask) == 0:
                    continue

                left_var = np.var(y[left_mask])
                right_var = np.var(y[right_mask])
                n_left = np.sum(left_mask)
                n_right = np.sum(right_mask)
                
                # Calculate variance reduction
                var_reduction = parent_var - (
                    (n_left * left_var + n_right * right_var) / n_samples
                )

                if var_reduction > best_var_reduction:
                    best_var_reduction = var_reduction
                    best_feature = feature_idx
                    best_threshold = threshold

        if best_var_reduction == -float("inf"):
            leaf_value = np.mean(y)
            return Node(value=leaf_value)

        # Create child splits
        left_mask = X[:, best_feature] <= best_threshold
        right_mask = ~left_mask
        
        left = self._grow_tree(X[left_mask], y[left_mask], depth + 1)
        right = self._grow_tree(X[right_mask], y[right_mask], depth + 1)

        return Node(
            feature=best_feature,
            threshold=best_threshold,
            left=left,
            right=right
        )

    def predict(self, X):
        return np.array([self._traverse_tree(x, self.root) for x in X])

    def _traverse_tree(self, x, node):
        if node.is_leaf_node():
            return node.value

        if x[node.feature] <= node.threshold:
            return self._traverse_tree(x, node.left)
        return self._traverse_tree(x, node.right)
        