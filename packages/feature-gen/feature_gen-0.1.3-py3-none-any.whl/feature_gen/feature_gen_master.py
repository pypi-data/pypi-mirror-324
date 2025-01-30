import datetime
from typing import List

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from feature_gen.implementation.constants import EnsembleMethod
from feature_gen.implementation.ensemble_classifier import EnsembleClassifier
from feature_gen.implementation.get_the_most_optimal_features_set import get_the_most_optimal_features_set
from feature_gen.utils.checker import check_if_this_is_classification_problem
from feature_gen.utils.df_preprocessor import DFPreprocessor


class FeatureGenMaster:

    def __init__(self, df: pd.DataFrame, target_column_name: str, min_number_of_target_unique_values: int = 20):
        self.df = df
        self._y = df[target_column_name]
        self._X = df.drop(columns=[target_column_name], axis=1)

        self._apply_one_hot_encoding_on_target_columns()

        if not check_if_this_is_classification_problem(
                y=self._y,
                min_number_of_target_unique_values=min_number_of_target_unique_values
        ):
            raise ValueError("This problem is not a classification problem.")

        self._all_best_features = {}
        self._best_original_features = {}
        self._best_new_features = {}

        self._average_all_ensemble_methods_scores = {}
        self._all_ensemble_methods_scores = {}

    def _apply_one_hot_encoding_on_target_columns(self) -> None:
        # This iis needed for Xgboost
        label_encoder = LabelEncoder()
        y = label_encoder.fit_transform(self._y)
        self._y = pd.DataFrame({self._y.name: y})

    def _pre_process_df(self) -> pd.DataFrame:
        df_preprocessor = DFPreprocessor(X=self._X)
        X = (
            df_preprocessor.
            drop_unnamed().
            drop_infinity().
            one_hot_encode().
            fill_nulls_with_mean().
            remove_potential_stratification().
            standardize_data().
            normalize_data().
            drop_highly_correlated_features().
            apply_transformations().
            get_final_X()
        )
        return X

    @staticmethod
    def _get_real_names_of_features(
            most_optimal_features_set: List[bool],
            pre_processed_and_transformed_X: pd.DataFrame
    ) -> List[str]:
        return [
            feature_name for feature_name, feature in
            zip(pre_processed_and_transformed_X.columns, most_optimal_features_set) if feature
        ]

    def _start(self, ensemble_methods: List[EnsembleMethod], **kwargs) -> None:
        test_size = kwargs.get('test_size', 0.2)
        random_state = kwargs.get('random_state', 42)

        dataset_original_features_count_before_ts = self._X.shape[1]
        pre_processed_and_transformed_X = self._pre_process_df()
        dataset_original_features_count_after_ts = pre_processed_and_transformed_X.shape[1]

        for ensemble_method in ensemble_methods:
            print(f"Ensemble method {ensemble_method} is being considered")
            date0 = datetime.datetime.now()
            X_train, X_test, y_train, y_test = train_test_split(
                pre_processed_and_transformed_X,
                self._y,
                test_size=test_size,
                random_state=random_state,
                stratify=self._y
            )
            most_optimal_features_set = get_the_most_optimal_features_set(
                X_train=X_train,
                y_train=y_train,
                ensemble_method=ensemble_method,
                **kwargs
            )

            new_X_train_for_most_optimal_features_set = X_train.iloc[:, most_optimal_features_set]
            new_X_test_for_most_optimal_features_set = X_test.iloc[:, most_optimal_features_set]

            ensemble_accuracies = EnsembleClassifier(
                X_train=new_X_train_for_most_optimal_features_set,
                X_test=new_X_test_for_most_optimal_features_set,
                y_train=y_train,
                y_test=y_test,
                **kwargs
            )
            ensemble_method_score, all_ensemble_ml_models_scores = ensemble_accuracies.run_for_individual(
                ensemble_method)
            r = {
                "dataset_original_features_count_before_ts": dataset_original_features_count_before_ts,
                "dataset_original_features_count_after_ts": dataset_original_features_count_after_ts,
                "dataset_features_count_after_whole_process": new_X_train_for_most_optimal_features_set.shape[1],
                "execution_time": (datetime.datetime.now() - date0).seconds,
                "ensemble_method_score": ensemble_method_score,
                "all_ensemble_ml_models_scores": all_ensemble_ml_models_scores
            }
            self._all_best_features[ensemble_method] = self._get_real_names_of_features(
                most_optimal_features_set=most_optimal_features_set,
                pre_processed_and_transformed_X=pre_processed_and_transformed_X,
            )
            self._all_ensemble_methods_scores[ensemble_method] = ensemble_method_score

        for ensemble_method in ensemble_methods:
            self._best_original_features[ensemble_method] = [
                f for f in self._all_best_features[ensemble_method] if f in self._X.columns
            ]
            self._best_new_features[ensemble_method] = [
                f for f in self._all_best_features[ensemble_method] if f not in self._X.columns
            ]

    def start(self, ensemble_methods: List[EnsembleMethod], **kwargs) -> None:
        self._start(ensemble_methods, **kwargs)

    def get_all_best_features(self):
        if not self._all_best_features:
            raise ValueError("You should call start() function first")
        return self._all_best_features

    def get_best_original_features(self):
        if not self._best_original_features:
            raise ValueError("You should call start() function first")
        return self._best_original_features

    def get_best_new_features(self):
        if not self._best_new_features:
            raise ValueError("You should call start() function first")
        return self._best_new_features

    def get_all_ensemble_methods_scores(self):
        if not self._all_ensemble_methods_scores:
            raise ValueError("You should call start() function first")
        return self._all_ensemble_methods_scores
