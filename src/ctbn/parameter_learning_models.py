import numpy as np
from sklearn.linear_model import LogisticRegression


class LRModel:

    @staticmethod
    def add_one(X, Y):
        num_samples = X.shape[0]
        idx = np.random.randint(num_samples)
        random_sample = X[idx]
        for val in (0,1):
            X = np.vstack([X, random_sample])
            Y = np.hstack([Y, val])
        return X, Y

    @staticmethod
    def get_cll(X, Y):
        if len(np.unique(Y)) == 1:
            X, Y = LRModel.add_one(X, Y)
        model = LogisticRegression(max_iter=1000, solver="liblinear")
        model.fit(X, Y)

        num_samples = X.shape[0]
        log_probability = model.predict_log_proba(X)
        log_likelihood = np.sum(log_probability[np.arange(num_samples), Y])
        return model, log_likelihood

    @staticmethod
    def get_cll_with_parents(X, Y):
        models = {}
        total_cll = 0
        for val in (0,1):
            X_val, Y_val = X[X[:,-1] == val], Y[X[:,-1] == val]
            model, cll = LRModel.get_cll(X_val, Y_val)
            models[val] = model
            total_cll+=cll
        return models, total_cll