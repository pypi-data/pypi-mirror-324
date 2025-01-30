from typing import Self

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler


class DFPreprocessor:
    def __init__(self, X: pd.DataFrame) -> None:
        self._X = X.copy()  # Store a copy to avoid modifying the original data
        self.__update_column_types()

    def __update_column_types(self):
        self._numeric_columns = self._X.select_dtypes(include='number').columns
        self._non_numeric_columns = self._X.select_dtypes(exclude='number').columns

    def drop_unnamed(self):
        if 'Unnamed: 0' in self._X.columns:
            self._X = self._X.drop(columns=['Unnamed: 0'])
        self.__update_column_types()
        return self

    def one_hot_encode(self) -> Self:
        """Converts all boolean and string columns into numeric format using one-hot encoding."""
        if isinstance(self._X, pd.DataFrame):
            # Apply one-hot encoding
            self._X = pd.get_dummies(self._X, columns=self._non_numeric_columns, drop_first=False)
        elif isinstance(self._X, np.ndarray):
            raise ValueError("For one-hot encoding, convert self._X to a DataFrame.")
        else:
            raise TypeError("self._X must be a pandas DataFrame for this operation.")
        return self

    def drop_infinity(self) -> Self:
        """Drop the rows with infinity."""
        self._X = self._X[~((self._X == np.inf) | (self._X == -np.inf)).any(axis=1)]
        self.__update_column_types()
        return self

    def fill_nulls_with_mean(self) -> Self:
        """Make the null values filled with the mean of the respective columns."""
        self._X = self._X.fillna(self._X.mean())
        return self

    # TODO: Maybe the question is a binary alssifcication
    def remove_potential_stratification(self) -> Self:
        """Removes potential stratification in the dataset."""
        # Assuming stratification means ensuring that the target variable is balanced or that there's no unintended bias
        # You can adjust the logic based on your specific definition of stratification
        # This is just an example of dropping any rows where the target column is the same as others.
        # Replace 'target' with the actual name of your target column if needed

        # if self._X[self._target_column_name].nunique() <= 2:
        #     self._X = self._X.drop(columns=[self._target_column_name])
        return self

    def standardize_data(self) -> Self:
        """Standardizes numerical columns to have a mean of 0 and standard deviation of 1."""
        # If we have no numeric columns, we simply skip over this step to avoid "ValueError: at least one array or dtype is required"
        if len(self._numeric_columns) == 0:
            return self
        scaler = StandardScaler()
        self._X[self._numeric_columns] = scaler.fit_transform(self._X[self._numeric_columns])
        return self

    def normalize_data(self) -> Self:
        """Normalizes numerical columns to be in the range [0, 1]."""
        # If we have no numeric columns, we simply skip over this step to avoid "ValueError: at least one array or dtype is required"
        if len(self._numeric_columns) == 0:
            return self
        scaler = MinMaxScaler()
        self._X[self._numeric_columns] = scaler.fit_transform(self._X[self._numeric_columns])
        return self

    def drop_highly_correlated_features(self, threshold=0.9) -> Self:
        """Removes columns with correlation greater than the threshold."""
        corr_matrix = self._X.corr().abs()
        upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
        to_drop = [column for column in upper.columns if any(upper[column] > threshold)]
        self._X = self._X.drop(columns=to_drop)
        self.__update_column_types()
        return self

    def apply_transformations(self) -> Self:
        if len(self._numeric_columns) == 0:
            return self

        epsilon = 1e-10
        transformed_cols = []

        # Attention. the transformations are applied only on originally numeric values
        for col in self._numeric_columns:
            # Calculate all transformations and store them in temporary DataFrames
            col_log = np.log(self._X[col] + np.abs(np.min(self._X[col])) + epsilon)
            col_squared = self._X[col] ** 2
            col_cubic = self._X[col] ** 3
            col_sqrt = np.sqrt(self._X[col] + np.abs(np.min(self._X[col])))
            col_cbrt = np.cbrt(self._X[col])

            # Sigmoid transformation (maps values to range [0, 1])
            z = (self._X[col] - self._X[col].min()) / (self._X[col].max() - self._X[col].min() + epsilon)
            z = 2 * z - 1
            col_sigmoid = 1 / (1 + np.exp(-z))

            # Tanh transformation (maps values to range [-1, 1])
            col_tanh = np.tanh(z)

            # Store each transformation in a list with appropriate column names
            transformed_cols.append(pd.DataFrame({
                f"{col}_log": col_log,
                f"{col}_squared": col_squared,
                f"{col}_cubic": col_cubic,
                f"{col}_sqrt": col_sqrt,
                f"{col}_cbrt": col_cbrt,
                f"{col}_sigmoid": col_sigmoid,
                f"{col}_tanh": col_tanh,
            }))

        # Concatenate all the transformed columns to the original DataFrame
        transformed_df = pd.concat(transformed_cols, axis=1)
        self._X = pd.concat([self._X, transformed_df], axis=1).copy()

        return self

    def get_final_X(self) -> pd.DataFrame:
        return self._X
