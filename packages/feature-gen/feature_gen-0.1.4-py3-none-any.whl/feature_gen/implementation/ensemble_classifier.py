import concurrent.futures
import random
import warnings

import numpy as np
import pandas as pd
from sklearn.exceptions import DataConversionWarning, ConvergenceWarning
from sklearn.kernel_approximation import RBFSampler
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.metrics import f1_score
from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier

from feature_gen.implementation.constants import EnsembleClassifierMLModel, EnsembleMethod

# Suppress only DataConversionWarning
warnings.filterwarnings("ignore", category=DataConversionWarning)
warnings.filterwarnings("ignore", category=ConvergenceWarning)


class EnsembleClassifier:
    """
    X_train here is after the reduction of the feature space . So this class is not responsible for ignoring the features
    """

    def __init__(self, X_train: pd.DataFrame, X_test: pd.DataFrame, y_train: pd.DataFrame, y_test: pd.DataFrame,
                 **kwargs):
        self._X_train = X_train
        self._X_test = X_test
        self._y_train = y_train
        self._y_test = y_test

        # Setting up defaults and overwriting with kwargs if provided
        random_state = kwargs.get('random_state', 42)
        max_iter = kwargs.get('max_iter', 500)
        C = kwargs.get('C', 1e5)
        solver = kwargs.get('solver', 'liblinear')
        gamma = kwargs.get('gamma', 1)
        n_components = kwargs.get('n_components', 100)
        sgd_loss = kwargs.get('sgd_loss', 'hinge')
        sgd_max_iter = kwargs.get('sgd_max_iter', 1000)
        sgd_tol = kwargs.get('sgd_tol', 1e-2)
        xgb_n_estimators = kwargs.get('xgb_n_estimators', 100)

        # Set the seed for Python's built-in random module
        random.seed(random_state)
        # Set the seed for NumPy
        np.random.seed(random_state)

        # Initialize models with either provided or default parameters
        self._logistic_reg = LogisticRegression(random_state=random_state, max_iter=max_iter, C=C, solver=solver)
        self._svm = Pipeline(steps=[
            ("rbf_feature", RBFSampler(gamma=gamma, random_state=random_state, n_components=n_components)),
            ("sgd_clf", SGDClassifier(loss=sgd_loss, max_iter=sgd_max_iter, tol=sgd_tol))
        ])
        self._xgb = XGBClassifier(random_state=random_state, n_estimators=xgb_n_estimators)

        self._result = {}

    def run_for_individual(self, ensemble_method: EnsembleMethod):
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            args = (self._X_train, self._y_train)
            res = {
                EnsembleClassifierMLModel.LOGISTIC_REG: executor.submit(self._logistic_reg.fit, *args),
                EnsembleClassifierMLModel.SVM: executor.submit(self._svm.fit, *args),
                EnsembleClassifierMLModel.XGBOOST: executor.submit(self._xgb.fit, *args)
            }

            for classifier, future in res.items():
                res[classifier] = future.result()

            predictions_dict = {}
            # Collect predictions from each classifier
            for classifier, model in res.items():
                predictions_dict[classifier] = model.predict(self._X_test)

        # 1. Greedy (Grd)
        if ensemble_method == EnsembleMethod.GREEDY:
            best_classifier = max(
                res.keys(),
                key=lambda clf: f1_score(self._y_test, predictions_dict[clf], average='macro')
            )
            self._result[EnsembleMethod.GREEDY] = predictions_dict[best_classifier]

        # 2. Averaging (Avg)
        if ensemble_method == EnsembleMethod.AVERAGING:
            avg_pred = np.mean(
                [predictions_dict[clf] for clf in res.keys()], axis=0
            )
            self._result[EnsembleMethod.AVERAGING] = np.round(avg_pred).astype(int)

        if ensemble_method == EnsembleMethod.WEIGHTED_AVERAGING:
            # 3. Weighted Averaging (Wavg)
            weights = {  # Weights based on accuracy
                clf: f1_score(self._y_test, predictions_dict[clf], average='macro')
                for clf in res.keys()
            }
            wavg_pred = np.average(
                [predictions_dict[clf] for clf in res.keys()], axis=0, weights=[weights[clf] for clf in res.keys()]
            )
            self._result[EnsembleMethod.WEIGHTED_AVERAGING] = np.round(wavg_pred).astype(int)

        # 4. Majority Voting
        if ensemble_method == EnsembleMethod.MAJORITY_VOTING:
            unique_classes = np.unique(self._y_train)
            majority_votes = np.zeros([len(res.keys()), self._X_test.shape[0], len(unique_classes)])
            idx = 0
            for clf in res.keys():
                for idxLabel in range(len(unique_classes)):
                    majority_votes[idx, predictions_dict[clf] == unique_classes[idxLabel], idxLabel] += 1
                idx += 1
            self._result[EnsembleMethod.MAJORITY_VOTING] = unique_classes[
                np.argmax(np.sum(majority_votes, axis=0), axis=1)
            ]

        # 5. Weighted Majority Voting (Wmv)
        if ensemble_method == EnsembleMethod.WEIGHTED_MAJORITY_VOTING:
            weights = {  # Weights based on accuracy
                clf: f1_score(self._y_test, predictions_dict[clf], average='macro')
                for clf in res.keys()
            }
            weighted_majority_votes = []
            for i in range(len(self._X_test)):
                class_votes = {}
                for clf in res.keys():
                    vote = predictions_dict[clf][i]
                    if vote not in class_votes:
                        class_votes[vote] = 0
                    class_votes[vote] += weights[clf]

                weighted_majority_votes.append(
                    max(class_votes, key=class_votes.get)
                )
            self._result[EnsembleMethod.WEIGHTED_MAJORITY_VOTING] = np.array(weighted_majority_votes)

        predicted_for_ensemble_method = self._result[ensemble_method]
        ensemble_method_score = f1_score(self._y_test, predicted_for_ensemble_method, average='macro')
        # Now based on all the ensemble methods we find the accuracy OR f1-score. We decided to go with f1-score
        all_ensemble_ml_models_scores = {
            cls: f1_score(self._y_test, predictions_dict[cls], average='macro') for cls, pred_set in
            predictions_dict.items()
        }
        return ensemble_method_score, all_ensemble_ml_models_scores
