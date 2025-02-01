import numpy as np

# Class representing a single node in the decision tree
class Node:
    def __init__(self, feature=None, threshold=None, left=None, right=None, value=None):
        # Feature index to split on
        self.feature = feature
        # Threshold value for the split
        self.threshold = threshold
        # Left child node
        self.left = left
        # Right child node
        self.right = right
        # Value if this is a leaf node
        self.value = value

# Class implementing the decision tree
class DecisionTree:
    def __init__(self, max_depth=None):
        # Maximum depth of the tree
        self.max_depth = max_depth
        # Root node of the tree
        self.root = None

    # Method to train the decision tree
    def fit(self, X, y):
        self.root = self._build_tree(X, y)

    # Method to make predictions for a dataset
    def predict(self, X):
        return np.array([self._traverse_tree(x, self.root) for x in X])

    # Recursive method to build the tree
    def _build_tree(self, X, y, depth=0):
        num_samples, num_features = X.shape
        num_labels = len(np.unique(y))

        # Stopping conditions
        if depth >= self.max_depth or num_labels == 1 or num_samples < 2:
            # Create a leaf node with the most common label
            leaf_value = self._most_common_label(y)
            return Node(value=leaf_value)

        # Find the best feature and threshold to split on
        best_feature, best_threshold = self._best_split(X, y)

        if best_feature is None:
            # Create a leaf node if no valid split is found
            leaf_value = self._most_common_label(y)
            return Node(value=leaf_value)

        # Split the data into left and right subsets
        left_indices = X[:, best_feature] <= best_threshold
        right_indices = X[:, best_feature] > best_threshold
        
        # Recursively build the left and right child nodes
        left_child = self._build_tree(X[left_indices], y[left_indices], depth + 1)
        right_child = self._build_tree(X[right_indices], y[right_indices], depth + 1)
        return Node(feature=best_feature, threshold=best_threshold, left=left_child, right=right_child)

    # Method to find the best feature and threshold for splitting
    def _best_split(self, X, y):
        num_samples, num_features = X.shape
        best_gini = float('inf')
        best_feature, best_threshold = None, None

        # Iterate over all features
        for feature in range(num_features):
            # Get unique values of the feature to use as thresholds
            thresholds = np.unique(X[:, feature])
            for threshold in thresholds:
                # Calculate Gini index for the split
                gini = self._gini_index(X, y, feature, threshold)
                if gini < best_gini:
                    best_gini = gini
                    best_feature = feature
                    best_threshold = threshold

        return best_feature, best_threshold

    # Method to calculate the Gini index for a split
    def _gini_index(self, X, y, feature, threshold):
        # Split the data into left and right subsets
        left_indices = X[:, feature] <= threshold
        right_indices = X[:, feature] > threshold

        # Return infinity if a subset is empty
        if len(y[left_indices]) == 0 or len(y[right_indices]) == 0:
            return float('inf')

        # Calculate Gini impurity for both subsets
        gini_left = self._gini(y[left_indices])
        gini_right = self._gini(y[right_indices])
        # Weighted Gini impurity of the split
        gini = (len(y[left_indices]) * gini_left + len(y[right_indices]) * gini_right) / len(y)
        return gini

    # Method to calculate the Gini impurity for a set of labels
    def _gini(self, y):
        # Proportions of each class
        proportions = [np.sum(y == c) / len(y) for c in np.unique(y)]
        # Gini impurity formula
        return 1 - sum([p ** 2 for p in proportions])

    # Method to find the most common label in a set
    def _most_common_label(self, y):
        return np.bincount(y).argmax()

    # Method to traverse the tree for a single sample
    def _traverse_tree(self, x, node):
        # Return the value if it's a leaf node
        if node.value is not None:
            return node.value

        # Traverse left or right based on the feature and threshold
        if x[node.feature] <= node.threshold:
            return self._traverse_tree(x, node.left)
        return self._traverse_tree(x, node.right)

