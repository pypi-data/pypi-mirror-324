from enum import Enum


class EnsembleClassifierMLModel(Enum):
    LOGISTIC_REG = "logistic_reg"
    SVM = "svm"
    XGBOOST = "xgboost"

    def __str__(self):
        return self.value

    def __repr__(self):
        return f"'{self.value}'"


class EnsembleMethod(Enum):
    GREEDY = "greedy"
    AVERAGING = "averaging"
    WEIGHTED_AVERAGING = "weighted_averaging"
    MAJORITY_VOTING = "majority_voting"
    WEIGHTED_MAJORITY_VOTING = "weighted_majority_voting"

    def __str__(self):
        return self.value

    def __repr__(self):
        return f"'{self.value}'"

class Transformations(Enum):
    LOG = 'log'
    SQUARE = 'square'
    CUBIC = 'cubic'
    SQUARE_ROOT = 'square_root'
    CUBIC_ROOT = 'cubic_root'
    SIGMOID = 'sigmoid'
    TANH = 'tanh'

    def __str__(self):
        return self.value

    def __repr__(self):
        return f"'{self.value}'"  # Represent the value in dict keys, etc.
