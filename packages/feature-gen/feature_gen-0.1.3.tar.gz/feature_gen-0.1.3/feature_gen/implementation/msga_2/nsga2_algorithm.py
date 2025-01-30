import random

import numpy as np
import pandas as pd
from deap import base, creator, tools

from feature_gen.implementation.constants import EnsembleMethod
from feature_gen.implementation.ensemble_classifier import EnsembleClassifier


def run_nsga_2_algorithm_for_dataset(
        X_train: pd.DataFrame,
        X_validation: pd.DataFrame,
        y_train: pd.DataFrame,
        y_validation: pd.DataFrame,
        ensemble_method: EnsembleMethod,
        **kwargs
):
    display_each_individual = kwargs.get("display_each_individual", True)
    generations_num = kwargs.get("generations_num", 5)
    first_population_size = kwargs.get("first_population_size", 10)

    def eval_features(individual):
        if display_each_individual:
            print(individual)
        # individual is like [0, 1, 0, 1, 0] so features_vector will be like [False, True, False, True, False]
        features_vector = [bool(i) for i in individual]
        assert len(features_vector) == len(individual)
        if features_vector.count(True) == 0:
            return 0, len(individual)  # Penalize having no features selected
        ensemble_for_individual = EnsembleClassifier(
            X_train=X_train.loc[:, features_vector],
            X_test=X_validation.loc[:, features_vector],
            y_train=y_train,
            y_test=y_validation,
            **kwargs
        )
        ensemble_method_score, all_ensemble_ml_models_scores = ensemble_for_individual.run_for_individual(ensemble_method)
        return ensemble_method_score, features_vector.count(True)

    # Check if 'FitnessMulti' and 'Individual' have already been created
    if not hasattr(creator, "FitnessMulti"):
        creator.create("FitnessMulti", base.Fitness, weights=(1.0, -1.0))

    if not hasattr(creator, "Individual"):
        creator.create("Individual", list, fitness=creator.FitnessMulti)

    toolbox = base.Toolbox()
    toolbox.register("attr_bool", random.randint, 0, 1)
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, n=X_train.shape[1])
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", eval_features)
    toolbox.register("mate", tools.cxUniform, indpb=0.5)
    toolbox.register("mutate", tools.mutFlipBit, indpb=0.02)
    toolbox.register("select", tools.selNSGA2)

    def inner_function():
        pop = toolbox.population(n=first_population_size)
        hof = tools.ParetoFront()
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", np.mean, axis=0)
        stats.register("std", np.std, axis=0)
        stats.register("min", np.min, axis=0)
        stats.register("max", np.max, axis=0)

        # Evaluate the initial population
        fitnesses = map(toolbox.evaluate, pop)
        for ind, fit in zip(pop, fitnesses):
            ind.fitness.values = fit

        # Genetic algorithm loop
        for gen in range(1, generations_num + 1):
            offspring = []
            while len(offspring) < len(pop):
                parent1, parent2 = random.sample(pop, 2)
                if random.random() < 1.0:  # Crossover probability is 1.0
                    child1, child2 = toolbox.clone(parent1), toolbox.clone(parent2)
                    toolbox.mate(child1, child2)
                    del child1.fitness.values
                    del child2.fitness.values
                    offspring.extend([child1, child2])
                if len(offspring) > len(pop):
                    offspring = offspring[:len(pop)]

            # Apply mutation
            for mutant in offspring:
                if random.random() < 0.02:
                    toolbox.mutate(mutant)
                    del mutant.fitness.values

            # Evaluate the offspring with invalid fitness
            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            for ind in invalid_ind:
                ind.fitness.values = toolbox.evaluate(ind)

            # Combine the population with offspring and select the best to form the new population
            pop[:] = toolbox.select(pop + offspring, len(pop))

            hof.update(pop)
            record = stats.compile(pop)
            if gen % 10 == 0:
                print(f"Generation {gen}: Stats {record}")

        return pop, stats, hof

    pop, stats, hof = inner_function()
    return pop, stats, hof
