from typing import List

import numpy as np
import pandas as pd

from feature_gen.implementation.msga_2.nsga2_algorithm import run_nsga_2_algorithm_for_dataset


def _create_bootstrap_samples(
        X_train: pd.DataFrame,
        y_train: pd.DataFrame,
        bootstrap_samples_count: int,
        random_state: int
):
    # Initialize lists to store bootstrap samples and out-of-bag (OOB) samples.
    samples = []
    samples_oob = []
    rng = np.random.RandomState(random_state)  # Initialize RNG only once

    for _ in range(bootstrap_samples_count):
        total_samples = X_train.shape[0]

        # Generate random indices with replacement to create a bootstrap sample
        indices = rng.choice(total_samples, total_samples, replace=True)

        # Identify the out-of-bag (OOB) indices (those not selected in the bootstrap sample)
        indices_out_of_bag = np.setdiff1d(np.arange(total_samples), indices)

        # Extract the bootstrap sample for both features (X) and labels (y)
        X_sample = X_train.iloc[indices]
        y_sample = y_train.iloc[indices]

        # Extract the out-of-bag sample for both features (X) and labels (y)
        X_oob_sample = X_train.iloc[indices_out_of_bag]
        y_oob_sample = y_train.iloc[indices_out_of_bag]

        # Append the bootstrap and OOB samples to their respective lists
        samples.append((X_sample, y_sample))
        samples_oob.append((X_oob_sample, y_oob_sample))

    # Return the lists of bootstrap samples and OOB samples
    # TODO: samples are for training and samples_oob for validation?
    return samples, samples_oob


def _macro_process(feature_sets):
    # Combine all the feature sets from the micro process -> union
    optimal_features_in = np.max(feature_sets, axis=0)

    return optimal_features_in


# Feature Set Aggregation: Combines feature subsets obtained from different runs of the genetic algorithm using majority voting.
def get_the_most_optimal_features_set(X_train, y_train, ensemble_method, **kwargs) -> List[bool]:
    bootstrap_samples_count = kwargs.get('bootstrap_samples_count', 2)
    random_state = kwargs.get('random_state', 42)

    bootstrap_samples, bootstrap_oob = _create_bootstrap_samples(X_train, y_train, bootstrap_samples_count,
                                                                 random_state)
    best_feature_sets = []

    for sample_i in range(bootstrap_samples_count):
        new_x_train, new_y_train = bootstrap_samples[sample_i]
        X_validation, y_validation = bootstrap_oob[sample_i]
        pop, stats, hof = run_nsga_2_algorithm_for_dataset(
            X_train=new_x_train,
            X_validation=X_validation,
            y_train=new_y_train,
            y_validation=y_validation,
            ensemble_method=ensemble_method,
            **kwargs
        )
        best_feature_sets.append((hof[0], stats))

    # Combine all best individuals from the micro stage. Here is our Fz
    combined_features = np.array([ind for ind, _ in best_feature_sets])

    combined_features = _macro_process(combined_features)

    features_vector = [bool(i) for i in combined_features]
    new_x_train, new_y_train = bootstrap_samples[0]
    X_validation, y_validation = bootstrap_oob[0]

    # Handle unexpected classes inside EnsembleClassifier
    pop, stats, hof = run_nsga_2_algorithm_for_dataset(
        X_train=new_x_train,
        X_validation=X_validation,
        y_train=new_y_train,
        y_validation=y_validation,
        ensemble_method=ensemble_method,
        **kwargs
    )
    new_optimal_features_vector = [bool(i) for i in hof[0]]
    # The length of new_optimal_features_vector may have decreased so we use
    # Asserting the features vector length has remained unchanged
    assert len(new_optimal_features_vector) == len(features_vector) == new_x_train.shape[1] == X_validation.shape[1]
    return new_optimal_features_vector
