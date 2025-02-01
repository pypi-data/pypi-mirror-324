import numpy as np
from cvxopt import matrix, solvers


class svm:
    def __init__(self):
        self.w = None
        self.b = None

    def fit(self, X, y):
        """
        Train the SVM model using quadratic programming.
        """
        n_samples, n_features = X.shape

        # Compute Gram matrix (Kernel: Linear)
        K = np.dot(X, X.T)

        # Convert y to a column vector
        y = y.reshape(-1, 1) * 1.0
        H = (y @ y.T) * K
        P = matrix(H)
        q = matrix(-np.ones((n_samples, 1)))
        G = matrix(-np.eye(n_samples))
        h = matrix(np.zeros(n_samples))
        A = matrix(y.T)
        b = matrix(0.0)

        # Solve quadratic programming problem
        solvers.options['show_progress'] = False
        solution = solvers.qp(P, q, G, h, A, b)
        alphas = np.array(solution['x']).flatten()

        # Support vectors have non-zero alpha
        sv = alphas > 1e-5
        self.w = np.sum(alphas[sv].reshape(-1, 1) * y[sv] * X[sv], axis=0)
        self.b = np.mean(y[sv] - np.dot(X[sv], self.w))

    def predict(self, X):
        """
        Predict the class labels for given input X.
        """
        return np.sign(np.dot(X, self.w) + self.b)

