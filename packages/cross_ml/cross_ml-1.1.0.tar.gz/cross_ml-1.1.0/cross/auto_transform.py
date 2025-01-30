import warnings
from datetime import datetime
from typing import Callable, List, Optional, Union

import numpy as np

from cross.auto_parameters.clean_data import (
    ColumnSelectionParamCalculator,
    MissingValuesParamCalculator,
    OutliersParamCalculator,
)
from cross.auto_parameters.feature_engineering import (
    CategoricalEncodingParamCalculator,
    CyclicalFeaturesTransformerParamCalculator,
    DateTimeTransformerParamCalculator,
    DimensionalityReductionParamCalculator,
    MathematicalOperationsParamCalculator,
    NumericalBinningParamCalculator,
)
from cross.auto_parameters.preprocessing import (
    NonLinearTransformationParamCalculator,
    NormalizationParamCalculator,
    QuantileTransformationParamCalculator,
    ScaleTransformationParamCalculator,
)
from cross.auto_parameters.shared import evaluate_model
from cross.transformations.utils.dtypes import numerical_columns
from cross.utils import get_transformer


def auto_transform(
    X: np.ndarray,
    y: np.ndarray,
    model,
    scoring: str,
    direction: str = "maximize",
    cv: Union[int, Callable] = None,
    groups: Optional[np.ndarray] = None,
    verbose: bool = True,
) -> List[dict]:
    """Automatically applies a series of data transformations to improve model performance.

    Args:
        X (np.ndarray): Feature matrix.
        y (np.ndarray): Target variable.
        model: Machine learning model with a fit method.
        scoring (str): Scoring metric for evaluation.
        direction (str, optional): "maximize" to increase score or "minimize" to decrease. Defaults to "maximize".
        cv (Union[int, Callable], optional): Number of cross-validation folds or a custom cross-validation generator. Defaults to None.
        groups (Optional[np.ndarray], optional): Group labels for cross-validation splitting. Defaults to None.
        verbose (bool, optional): Whether to print progress messages. Defaults to True.

    Returns:
        List[dict]: A list of applied transformations.
    """
    if verbose:
        date_time = _date_time()
        print(f"\n[{date_time}] Starting experiment to find the best transformations")
        print(f"[{date_time}] Data shape: {X.shape}")
        print(f"[{date_time}] Model: {model.__class__.__name__}")
        print(f"[{date_time}] Scoring: {scoring}\n")

    X = X.copy()
    orig_num_columns = numerical_columns(X)

    transformations = []
    calculators = _initialize_calculators()

    scores = []
    score = evaluate_model(X, y, model, scoring, cv, groups)
    scores.append(("Base", score))

    with warnings.catch_warnings():
        warnings.filterwarnings("ignore")

        for name, calculator in calculators:
            if verbose:
                print(f"[{_date_time()}] Fitting transformation: {name}")

            columns_to_select = (
                orig_num_columns
                if name in ["NumericalBinning", "MathematicalOperations"]
                else X.columns
            )
            columns_to_select = list(set(columns_to_select).intersection(X.columns))

            transformation = calculator.calculate_best_params(
                X.loc[:, columns_to_select],
                y,
                model,
                scoring,
                direction,
                cv,
                groups,
                verbose,
            )

            if transformation:
                transformations.append(transformation)
                transformer = get_transformer(
                    transformation["name"], transformation["params"]
                )

                score = evaluate_model(X, y, model, scoring, cv, groups, transformer)
                scores.append((name, score))

                X = transformer.fit_transform(X, y)

    for name, score in scores:
        print(f"{name}: {score}")

    return transformations


def _date_time() -> str:
    return datetime.now().strftime("%Y/%m/%d %H:%M:%S")


def _initialize_calculators():
    return [
        ("MissingValuesHandler", MissingValuesParamCalculator()),
        ("OutliersHandler", OutliersParamCalculator()),
        ("DateTimeTransformer", DateTimeTransformerParamCalculator()),
        ("CyclicalFeaturesTransformer", CyclicalFeaturesTransformerParamCalculator()),
        ("CategoricalEncoding", CategoricalEncodingParamCalculator()),
        ("NonLinearTransformation", NonLinearTransformationParamCalculator()),
        ("NumericalBinning", NumericalBinningParamCalculator()),
        ("ScaleTransformation", ScaleTransformationParamCalculator()),
        ("Normalization", NormalizationParamCalculator()),
        ("QuantileTransformation", QuantileTransformationParamCalculator()),
        ("MathematicalOperations", MathematicalOperationsParamCalculator()),
        ("DimensionalityReduction", DimensionalityReductionParamCalculator()),
        ("ColumnSelection", ColumnSelectionParamCalculator()),
    ]
