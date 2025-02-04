import numpy as np

class Node:
    def __init__(self, value=None, left=None, right=None):
        self.value = value
        self.split_feature = None
        self.split_value = None
        self.left = left
        self.right = right


""" 
    these are the following helper function to build a Decision tree regressor.
        1. _build_tree
        2. _find_best_split
        3. _compute_gain
        4. _predict_single
        
    1.fit
    2.predict
"""
class DecisionTreeRegressor:
    def __init__(self, max_depth=3, min_samples_split=2):
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split  # Minimum samples required to split
        self.tree = None

    #here the y is the residual
    def fit(self, X, y): 
        if X.ndim == 1:  
            X = X.reshape(-1, 1)
        
        self.tree = self._build_tree(X, y)


    def _build_tree(self, X, y,  depth=0):
        if len(set(y)) == 1 or depth >= self.max_depth:
            return Node(value=np.mean(y))

        best_split = self._find_best_split(X, y)
        if best_split is None:
            return Node(value=np.mean(y))

        split_feature = best_split['feature']
        split_value = best_split['value']
        
        if isinstance(split_value, np.ndarray):
            if split_value.size == 1:
                split_value = split_value.item()  
            else:
                raise ValueError(f"Unexpected shape for split_value: {split_value.shape}")

        left_mask = X[:, split_feature] <= split_value
        right_mask = ~left_mask

        # Ensure we have enough samples to continue splitting
        if np.sum(left_mask) < self.min_samples_split or np.sum(right_mask) < self.min_samples_split:
            return Node(value=np.mean(y))

        left_node = self._build_tree(X[left_mask], y[left_mask], depth + 1)
        right_node = self._build_tree(X[right_mask], y[right_mask],  depth + 1)

        node = Node(left=left_node, right=right_node)
        node.split_feature = split_feature
        node.split_value = split_value

        return node

    

    def _find_best_split(self, X, y):
        best_gain = -float('inf')
        best_split = None

        for feature_index in range(X.shape[1]):
            sorted_indices = np.argsort(X[:, feature_index], axis=0)
            X_sorted = X[sorted_indices].reshape(-1, X.shape[1])
            y_sorted = y[sorted_indices]
            
            for i in range(1, len(X_sorted)):
                if (X_sorted[i] == X_sorted[i - 1]).all():
                    continue
                
                left_y = y_sorted[:i]
                right_y = y_sorted[i:]

                if len(left_y) > 0 and len(right_y) > 0:
                    gain = self._compute_gain(left_y, right_y, y)
                    
                    if gain > best_gain:
                        best_gain = gain
                        # Ensure best_split['value'] is a scalar
                        best_split_value = X_sorted[i, feature_index]  # Select the scalar value from the sorted array
                        best_split = {'feature': feature_index, 'value': best_split_value}

        return best_split

    
    

    def _compute_gain(self, left_y, right_y, y, _lambda = 1):
        if len(left_y) == 0 or len(right_y) == 0:
            return 0  # Return no gain if either side is empty
        
        def similarity_score(residuals):
            return (np.sum(residuals) ** 2) / (len(residuals) + _lambda) 
        
        root_similarity = similarity_score(y)
        left_similarity = similarity_score(left_y) if len(left_y) > 0 else 0
        right_similarity = similarity_score(right_y) if len(right_y) > 0 else 0

        gain = left_similarity + right_similarity - root_similarity
        return gain
        


    def predict(self, X):
        return np.array([self._predict_single(x, self.tree) for x in X])
    
    
    
    def _predict_single(self, x, node):
        if node.left is None and node.right is None:
            return node.value

        if x[node.split_feature] <= node.split_value:
            return self._predict_single(x, node.left)
        else:
            return self._predict_single(x, node.right)