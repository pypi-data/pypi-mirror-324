import pandas as pd
import numpy as np


def check_if_this_is_classification_problem(
        y: pd.DataFrame,
        min_number_of_target_unique_values: int = 20
) -> bool:
    """
    Determines if a given problem is a classification problem based on the number of unique target values.

    Args:
        y (pd.DataFrame): The target values in a DataFrame or Series format.
        min_number_of_target_unique_values (int): The minimum number of unique target values to consider the problem
                                                  as regression rather than classification.

    Returns:
        bool: True if the problem is a classification problem, False otherwise.
    """
    if not isinstance(y, (pd.Series, pd.DataFrame, np.ndarray)):
        raise ValueError("The target 'y' must be a pandas Series, DataFrame, or numpy array.")

    # Convert DataFrame or 2D array to 1D array
    if isinstance(y, pd.DataFrame):
        if y.shape[1] != 1:
            raise ValueError("The target 'y' DataFrame must contain exactly one column.")
        y = y.squeeze()  # Convert DataFrame to Series

    # Ensure y is 1D
    if len(y.shape) > 1:
        y = y.ravel()  # Flatten to 1D

    # Count unique values in the target
    num_unique_values = pd.Series(y).nunique()

    # Classification is determined if unique values are fewer than the threshold
    return num_unique_values < min_number_of_target_unique_values
