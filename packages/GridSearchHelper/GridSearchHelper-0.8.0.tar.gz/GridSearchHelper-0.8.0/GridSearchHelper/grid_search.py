# grid_search.py

from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import (
    RandomForestClassifier,
    GradientBoostingClassifier,
    HistGradientBoostingClassifier,
    AdaBoostClassifier,
    ExtraTreesClassifier,
    BaggingClassifier,
)
from sklearn.svm import SVC, LinearSVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import (
    LogisticRegression,
    RidgeClassifier,
    SGDClassifier,
    PassiveAggressiveClassifier,
)
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB, BernoulliNB, MultinomialNB
from sklearn.neural_network import MLPClassifier
from sklearn.discriminant_analysis import (
    LinearDiscriminantAnalysis,
    QuadraticDiscriminantAnalysis,
)
from typing import Dict, Optional, Union, Tuple, Any
import numpy as np
from numpy.typing import ArrayLike


def get_param_grid(
    model: str,
    additional_params: Optional[Dict[str, Union[int, float, list]]] = None,
) -> Dict[str, list]:
    """
    Seçilən modelə uyğun hiperparametr gridini qaytarır.

    Args:
        model (str): Modelin adı.
        additional_params (dict, optional): Əlavə parametrlər.

    Returns:
        dict: Parametrlər gridini qaytarır.

    Nümunə:
        >>> get_param_grid('RandomForestClassifier', {'n_estimators': [100, 200]})
        {'n_estimators': [100, 200], 'max_depth': [...]}
    """
    param_grids = {
        "RandomForestClassifier": {
            "n_estimators": [50, 100, 200, 300],
            "max_depth": [5, 10, 15, 20, None],
            "min_samples_split": [2, 5, 10],
            "min_samples_leaf": [1, 2, 4],
            "max_features": ["sqrt", "log2", None],
            "bootstrap": [True, False],
        },
        "GradientBoosting": {
            "n_estimators": [50, 100, 200, 300],
            "learning_rate": [0.01, 0.05, 0.1, 0.2],
            "max_depth": [3, 5, 7, 9],
            "subsample": [0.8, 0.9, 1.0],
            "min_samples_split": [2, 5, 10],
            "min_samples_leaf": [1, 2, 4],
        },
        "HistGradientBoosting": {
            "max_iter": [50, 100, 200, 300],
            "learning_rate": [0.01, 0.1, 0.2],
            "max_depth": [3, 5, 7, 9],
            "min_samples_leaf": [1, 5, 20],
            "l2_regularization": [0, 1.0, 10.0],
        },
        "AdaBoost": {
            "n_estimators": [50, 100, 200],
            "learning_rate": [0.01, 0.1, 1.0],
            "algorithm": ["SAMME", "SAMME.R"],
        },
        "ExtraTrees": {
            "n_estimators": [50, 100, 200],
            "max_depth": [5, 10, 15, None],
            "min_samples_split": [2, 5, 10],
            "min_samples_leaf": [1, 2, 4],
            "max_features": ["sqrt", "log2", None],
        },
        "Bagging": {
            "n_estimators": [10, 30, 50, 100],
            "max_samples": [0.5, 0.7, 1.0],
            "max_features": [0.5, 0.7, 1.0],
            "bootstrap": [True, False],
            "bootstrap_features": [True, False],
        },
        "SVC": {
            "C": [0.1, 1, 10, 100, 1000],
            "kernel": ["linear", "rbf", "poly", "sigmoid"],
            "gamma": ["scale", "auto", 0.1, 1, 10],
            "degree": [2, 3, 4, 5],
            "coef0": [0.0, 0.1, 0.5, 1.0],
        },
        "LinearSVC": {
            "C": [0.1, 1, 10],
            "penalty": ["l1", "l2"],
            "dual": [True, False],
            "max_iter": [1000, 2000, 5000],
        },
        "KNeighbors": {
            "n_neighbors": [3, 5, 7, 9, 11],
            "weights": ["uniform", "distance"],
            "metric": ["euclidean", "manhattan", "minkowski"],
            "p": [1, 2],
            "leaf_size": [10, 30, 50],
        },
        "LogisticRegression": {
            "C": [0.001, 0.01, 0.1, 1, 10],
            "penalty": ["l1", "l2", "elasticnet"],
            "solver": ["liblinear", "saga", "newton-cg", "lbfgs"],
            "max_iter": [1000, 2000, 5000],
            "l1_ratio": [0.2, 0.5, 0.8],
        },
        "RidgeClassifier": {
            "alpha": [0.1, 1.0, 10.0, 100.0],
            "solver": ["auto", "svd", "cholesky", "sparse_cg"],
            "max_iter": [None, 1000, 2000],
        },
        "SGDClassifier": {
            "loss": ["hinge", "log_loss", "modified_huber"],
            "penalty": ["l1", "l2", "elasticnet"],
            "alpha": [0.0001, 0.001, 0.01],
            "max_iter": [1000, 2000, 5000],
            "learning_rate": ["constant", "optimal", "adaptive"],
        },
        "PassiveAggressive": {
            "C": [0.1, 1.0, 10.0],
            "max_iter": [1000, 2000, 5000],
            "early_stopping": [True, False],
            "validation_fraction": [0.1, 0.2],
        },
        "DecisionTree": {
            "max_depth": [5, 10, 15, 20, None],
            "min_samples_split": [2, 5, 10],
            "min_samples_leaf": [1, 2, 4],
            "max_features": ["sqrt", "log2", None],
            "criterion": ["gini", "entropy"],
        },
        "GaussianNB": {"var_smoothing": [1e-9, 1e-8, 1e-7, 1e-6]},
        "BernoulliNB": {
            "alpha": [0.1, 0.5, 1.0, 2.0],
            "binarize": [0.0, 0.5, None],
            "fit_prior": [True, False],
        },
        "MultinomialNB": {"alpha": [0.1, 0.5, 1.0, 2.0], "fit_prior": [True, False]},
        "MLPClassifier": {
            "hidden_layer_sizes": [(50,), (100,), (50, 50), (100, 50), (100, 100)],
            "activation": ["relu", "tanh", "logistic"],
            "solver": ["adam", "sgd", "lbfgs"],
            "alpha": [0.0001, 0.001, 0.01, 0.1],
            "learning_rate": ["constant", "adaptive", "invscaling"],
            "max_iter": [1000, 2000, 5000],
        },
        "LinearDiscriminantAnalysis": {
            "solver": ["svd", "lsqr", "eigen"],
            "shrinkage": [None, "auto", 0.1, 0.5, 0.9],
        },
        "QuadraticDiscriminantAnalysis": {
            "reg_param": [0.0, 0.1, 0.2, 0.5],
            "tol": [1e-4, 1e-3, 1e-2],
        },
    }

    if additional_params:
        if model not in param_grids:
            raise ValueError(f"Model '{model}' üçün parametrlər tapılmadı.")
        param_grids[model].update(additional_params)

    if model not in param_grids:
        raise ValueError(
            f"Model adı '{model}' düzgün deyil. Mövcud modellər: {', '.join(param_grids.keys())}."
        )

    return param_grids[model]


def perform_grid_search(
    model: str,
    X_train: ArrayLike,
    y_train: ArrayLike,
    additional_params: Optional[Dict[str, Any]] = None,
    cv_folds: int = 5,
    scoring: Optional[Union[str, callable]] = None,
    verbose: int = 0,
    n_jobs: int = -1,
) -> Tuple[Dict[str, Any], float, GridSearchCV]:
    """
    Seçilən model adı ilə GridSearchCV tətbiq edir və ən yaxşı hiperparametrləri tapır.

    Args:
        model (str): Modelin adı.
        X_train (array-like): Təlim verilənlərinin xüsusiyyətləri.
        y_train (array-like): Təlim verilənlərinin hədəf dəyişəni.
        additional_params (dict, optional): Əlavə parametrlər.
        cv_folds (int): Cross-validation üçün fold sayı. Default 5.
        scoring (str or callable, optional): Qiymətləndirmə metrikası.
        verbose (int): Əlavə məlumatların çap edilməsi səviyyəsi.
        n_jobs (int): Paralel işləmə üçün prosessor nüvələri sayı.

    Returns:
        tuple: Ən yaxşı parametrlər, ən yaxşı skor və GridSearchCV obyekti.

    Nümunə:
        >>> best_params, best_score, grid = perform_grid_search('RandomForestClassifier', X, y)
    """
    models_mapping = {
        "RandomForestClassifier": RandomForestClassifier,
        "GradientBoosting": GradientBoostingClassifier,
        "HistGradientBoosting": HistGradientBoostingClassifier,
        "AdaBoost": AdaBoostClassifier,
        "ExtraTrees": ExtraTreesClassifier,
        "Bagging": BaggingClassifier,
        "SVC": SVC,
        "LinearSVC": LinearSVC,
        "KNeighbors": KNeighborsClassifier,
        "LogisticRegression": LogisticRegression,
        "RidgeClassifier": RidgeClassifier,
        "SGDClassifier": SGDClassifier,
        "PassiveAggressive": PassiveAggressiveClassifier,
        "DecisionTree": DecisionTreeClassifier,
        "GaussianNB": GaussianNB,
        "BernoulliNB": BernoulliNB,
        "MultinomialNB": MultinomialNB,
        "MLPClassifier": MLPClassifier,
        "LinearDiscriminantAnalysis": LinearDiscriminantAnalysis,
        "QuadraticDiscriminantAnalysis": QuadraticDiscriminantAnalysis,
    }

    if model not in models_mapping:
        raise ValueError(
            f"Model '{model}' dəstəklənmir. Mövcud modellər: {', '.join(models_mapping.keys())}."
        )

    model_class = models_mapping[model]
    model = model_class()

    param_grid = get_param_grid(model, additional_params)

    grid_search = GridSearchCV(
        estimator=model,
        param_grid=param_grid,
        cv=cv_folds,
        scoring=scoring,
        verbose=verbose,
        n_jobs=n_jobs,
    )

    grid_search.fit(X_train, y_train)

    return grid_search.best_params_, grid_search.best_score_, grid_search
