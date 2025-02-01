# Feature-Gen: A Robust Feature Engineering Framework

**Feature-Gen** is a Python-based library designed to simplify and optimize feature engineering for classification tasks. By integrating genetic algorithms, ensemble learning, and advanced feature transformations, Feature-Gen enables the discovery of feature subsets that maximize model performance while ensuring interpretability. It supports efficient processing through multithreading and multiprocessing, making it scalable for large datasets.

---

## Key Features

- **Automated Feature Engineering**: Automatically identifies and optimizes feature subsets for classification tasks.
- **Advanced Transformations**: Includes transformations like logarithmic, square, cubic, sigmoid, and tanh to uncover complex, non-linear relationships.
- **Multi-objective Optimization**: Leverages the NSGA-II genetic algorithm to optimize both classification accuracy and feature subset size.
- **Ensemble Learning Integration**: Combines Logistic Regression, SVM, and XGBoost to ensure diverse model perspectives.
- **Flexible Ensemble Methods**: Supports strategies like Majority Voting, Weighted Averaging, and Greedy Selection for robust feature evaluation.
- **Scalable Architecture**: Uses multithreading and multiprocessing to handle large datasets efficiently.
- **Extensive Validation**: Tested on over 100 datasets, demonstrating robustness and adaptability across domains.

---

## Installation

Install the library directly from PyPI:

```bash
pip install feature-gen
```

---

## Getting Started

### Example Usage

The following example demonstrates how to use Feature-Gen to perform feature engineering:

```python
# Example Dataset
import pandas as pd
from feature_gen.feature_gen_master import FeatureGenMaster
from feature_gen.implementation.constants import EnsembleMethod
from sklearn.datasets import load_wine

# Load and prepare dataset
data = load_wine()
df = pd.DataFrame(data.data, columns=data.feature_names)
df['target'] = data.target

# Show the current features
print(df.columns)

# Initialize FeatureGenMaster
f_g = FeatureGenMaster(df, 'target')

# Start the feature engineering process
f_g.start(
    ensemble_methods=[EnsembleMethod.GREEDY, EnsembleMethod.WEIGHTED_AVERAGING]
)

# Retrieve results
print("Best New Features:", f_g.get_best_new_features())
print("Best Original Features:", f_g.get_best_original_features())
print("All Ensemble Methods Scores:", f_g.get_all_ensemble_methods_scores())
```

The following example demonstrates how to use Feature-Gen to perform feature engineering with full control over the library

```python
import pandas as pd
from sklearn.datasets import load_wine

from feature_gen.feature_gen_master import FeatureGenMaster
from feature_gen.implementation.constants import EnsembleMethod

all_ensemble_methods = [
    EnsembleMethod.GREEDY,
    EnsembleMethod.WEIGHTED_MAJORITY_VOTING
]

# Load the Iris dataset
data = load_wine()

# Create a DataFrame with the features and target
df = pd.DataFrame(data.data, columns=data.feature_names)
df['target'] = data.target

# Show the current features
print(df.columns)

f_g = FeatureGenMaster(df, 'target', min_number_of_target_unique_values=20)

f_g.start(
    ensemble_methods=all_ensemble_methods,
    random_state=42,
    max_iter=50,
    C=1e5,
    solver='liblinear',
    gamma=1,
    n_components=100,
    sgd_loss='hinge',
    sgd_max_iter=1000,
    sgd_tol=1e-2,
    xgb_n_estimators=100,
    generations_num=2,
    bootstrap_samples_count=1,
    first_population_size=4
)

print('Best new features', f_g.get_best_new_features())
print('Best original features', f_g.get_best_original_features())
print('Best all features', f_g.get_all_best_features())
print("All ensemble methods scores", f_g.get_all_ensemble_methods_scores())
```

---

## Framework Architecture

### 1. **Micro-Step Genetic Algorithm**
- **Bootstrap Sampling**: Generates three independent bootstrap samples to ensure robustness and diversity.
- **Population Initialization**: Creates a population of binary chromosomes representing feature subsets.
- **Evaluation Metrics**:
  - Maximizes the F1 score of an ensemble model (Logistic Regression, SVM, XGBoost).
  - Minimizes the number of selected features for interpretability.
- **Genetic Operations**:
  - **Selection**: Binary tournament selection to choose the best chromosomes.
  - **Crossover**: Uniform crossover for generating offspring.
  - **Mutation**: Flip-bit mutation to introduce diversity.
  - **Population Update**: Combines parents and offspring using NSGA-II for multi-objective optimization.

### 2. **Macro-Step Genetic Algorithm**
- **Feature Aggregation**: Combines feature subsets from the micro-step using union logic.
- **Global Optimization**: Refines the macro-feature set using NSGA-II.
- **Final Feature Set**: Outputs an optimal feature set balancing accuracy and interpretability.

---

## Core Features and Functionality

- **Multithreading and Multiprocessing**:
  - Uses multithreading for concurrent evaluations and multiprocessing for parallelizing resource-intensive tasks.
  - Ensures scalability and efficient execution for large datasets.

- **Built-in Ensemble Methods**:
  - Supports flexible aggregation strategies like Majority Voting, Weighted Averaging, and Greedy Selection.

- **Advanced Feature Transformations**:
  - Includes transformations such as logarithmic, sigmoid, and tanh to capture non-linear relationships.

- **Extensive Validation**:
  - Tested on over 100 datasets, ensuring robustness and reliability.

---

## Strengths

1. **Robust Optimization**: Balances competing objectives through the micro-macro genetic algorithm.
2. **Integration of Transformations**: Enhances predictive performance by uncovering non-linear relationships.
3. **Generalizability**: Ensures applicability across linear, boundary-based, and non-linear problems.
4. **Interpretability**: Achieves significant feature set reductions without compromising accuracy.

---

## Future Directions

1. **Scalability Enhancements**: Expand support for distributed systems to handle even larger datasets.
2. **Dynamic Transformation Framework**: Introduce dataset-specific transformation selection for enhanced adaptability.
3. **Additional Ensemble Methods**: Integrate more aggregation strategies to improve robustness and flexibility.
4. **User Interface**: Develop visualization tools for better insights into feature engineering results.

---

## Resources

- **Documentation**: Available on PyPI: [Feature-Gen Documentation](https://pypi.org/project/feature-gen/)
- **Source Code**: Hosted on your development repository.

---

## Contributing

Contributions are welcome! For major changes, please open an issue to discuss proposed updates. Ensure all pull requests align with the project's goals and include relevant tests.

---

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
