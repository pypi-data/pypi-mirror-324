import numpy as np
from tqdm import tqdm
from .decision_tree_reg import My_DecisionTree_Regressor


class My_XGBClassifier:
    def __init__(self, n_estimators=100, learning_rate=0.1, max_depth=1):
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.max_depth = max_depth
        self.models = []  # Stores weak learners
        self.gamma_values = []

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def log_loss_gradient(self, y, p):
        return y - p  #

    def fit(self, X, y):
        y = y * 2 - 1  # Convert labels from {0,1} to {-1,1} for boosting

        # Step 1: Initialize F_0 with prior probability
        F_m = np.full(y.shape, np.log(np.mean(y == 1) / np.mean(y == -1)))

        for _ in tqdm(range(self.n_estimators)):
            # Compute residuals
            p_m = self.sigmoid(F_m)
            residuals = self.log_loss_gradient(y, p_m)

            # Train a weak learner on residuals
            tree = My_DecisionTree_Regressor(max_depth=self.max_depth)
            tree.fit(X, residuals)

            # Compute optimal step size gamma_m
            predicted_residuals = tree.predict(X)

            gamma_m = np.sum(residuals * predicted_residuals) / np.sum(
                predicted_residuals**2 + 1e-6
            )

            #  Update the model
            F_m += self.learning_rate * gamma_m * predicted_residuals

            # Store tree and gamma
            self.models.append(tree)
            self.gamma_values.append(gamma_m)


    def predict_proba(self, X):
        F_m = np.full(X.shape[0], np.log(0.5 / 0.5))

        for tree, gamma in zip(self.models, self.gamma_values):
            F_m += self.learning_rate * gamma * tree.predict(X)

        return self.sigmoid(F_m)

    def predict(self, X):
        return (self.predict_proba(X) >= 0.5).astype(int)
