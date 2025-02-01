from __future__ import annotations

from itertools import product
from typing import Callable, Literal

import numpy as np
import pytest
import sklearn.datasets
import torch
from sklearn.base import check_is_fitted
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.utils.estimator_checks import parametrize_with_checks

from tabpfn import TabPFNRegressor
from tabpfn.preprocessing import PreprocessorConfig

devices = ["cpu"]
if torch.cuda.is_available():
    devices.append("cuda")

feature_shift_decoders = ["shuffle", "rotate"]
fit_modes = [
    "low_memory",
    "fit_preprocessors",
    "fit_with_cache",
]
inference_precision_methods = ["auto", "autocast", torch.float64]
remove_remove_outliers_stds = [None, 12]

all_combinations = list(
    product(
        devices,
        feature_shift_decoders,
        fit_modes,
        inference_precision_methods,
        remove_remove_outliers_stds,
    ),
)


# Wrap in fixture so it's only loaded in if a test using it is run
@pytest.fixture(scope="module")
def X_y() -> tuple[np.ndarray, np.ndarray]:
    X, y = sklearn.datasets.fetch_california_housing(return_X_y=True)
    X, y = X[:100], y[:100]
    return X, y  # type: ignore


@pytest.mark.parametrize(
    (
        "device",
        "feature_shift_decoder",
        "fit_mode",
        "inference_precision",
        "remove_outliers_std",
    ),
    all_combinations,
)
def test_regressor(
    device: Literal["cuda", "cpu"],
    feature_shift_decoder: Literal["shuffle", "rotate"],
    fit_mode: Literal["low_memory", "fit_preprocessors", "fit_with_cache"],
    inference_precision: torch.types._dtype | Literal["autocast", "auto"],
    remove_outliers_std: int | None,
    X_y: tuple[np.ndarray, np.ndarray],
) -> None:
    if device == "cpu" and inference_precision == "autocast":
        pytest.skip("Only GPU supports inference_precision")

    model = TabPFNRegressor(
        n_estimators=2,
        device=device,
        fit_mode=fit_mode,
        inference_precision=inference_precision,
        inference_config={
            "OUTLIER_REMOVAL_STD": remove_outliers_std,
            "FEATURE_SHIFT_METHOD": feature_shift_decoder,
        },
    )

    X, y = X_y

    returned_model = model.fit(X, y)
    assert returned_model is model, "Returned model is not the same as the model"
    check_is_fitted(returned_model)

    # Should not fail prediction
    predictions = model.predict(X)
    assert predictions.shape == (X.shape[0],), "Predictions shape is incorrect"

    # check different modes
    predictions = model.predict(X, output_type="median")
    assert predictions.shape == (X.shape[0],), "Predictions shape is incorrect"
    predictions = model.predict(X, output_type="mode")
    assert predictions.shape == (X.shape[0],), "Predictions shape is incorrect"
    quantiles = model.predict(X, output_type="quantiles", quantiles=[0.1, 0.9])
    assert isinstance(quantiles, list)
    assert len(quantiles) == 2
    assert quantiles[0].shape == (X.shape[0],), "Predictions shape is incorrect"


# TODO(eddiebergman): Should probably run a larger suite with different configurations
@parametrize_with_checks([TabPFNRegressor()])
def test_sklearn_compatible_estimator(
    estimator: TabPFNRegressor,
    check: Callable[[TabPFNRegressor], None],
) -> None:
    if check.func.__name__ in (  # type: ignore
        "check_methods_subset_invariance",
        "check_methods_sample_order_invariance",
    ):
        estimator.inference_precision = torch.float64
    if check.func.__name__ == "check_methods_sample_order_invariance":  # type: ignore
        pytest.xfail("We're not at 1e-7 difference yet")
    check(estimator)


def test_regressor_in_pipeline(X_y: tuple[np.ndarray, np.ndarray]) -> None:
    """Test that TabPFNRegressor works correctly within a sklearn pipeline."""
    X, y = X_y

    # Create a simple preprocessing pipeline
    pipeline = Pipeline(
        [
            ("scaler", StandardScaler()),
            (
                "regressor",
                TabPFNRegressor(
                    n_estimators=2,  # Fewer estimators for faster testing
                ),
            ),
        ],
    )

    pipeline.fit(X, y)
    predictions = pipeline.predict(X)

    # Check predictions shape
    assert predictions.shape == (X.shape[0],), "Predictions shape is incorrect"

    # Test different prediction modes through the pipeline
    predictions_median = pipeline.predict(X, output_type="median")
    assert predictions_median.shape == (
        X.shape[0],
    ), "Median predictions shape is incorrect"

    predictions_mode = pipeline.predict(X, output_type="mode")
    assert predictions_mode.shape == (
        X.shape[0],
    ), "Mode predictions shape is incorrect"

    quantiles = pipeline.predict(X, output_type="quantiles", quantiles=[0.1, 0.9])
    assert isinstance(quantiles, list)
    assert len(quantiles) == 2
    assert quantiles[0].shape == (
        X.shape[0],
    ), "Quantile predictions shape is incorrect"


def test_dict_vs_object_preprocessor_config(X_y: tuple[np.ndarray, np.ndarray]) -> None:
    """Test that dict configs behave identically to PreprocessorConfig objects."""
    X, y = X_y

    # Define same config as both dict and object
    dict_config = {
        "name": "quantile_uni",
        "append_original": False,  # changed from default
        "categorical_name": "ordinal_very_common_categories_shuffled",
        "global_transformer_name": "svd",
        "subsample_features": -1,
    }

    object_config = PreprocessorConfig(
        name="quantile_uni",
        append_original=False,  # changed from default
        categorical_name="ordinal_very_common_categories_shuffled",
        global_transformer_name="svd",
        subsample_features=-1,
    )

    # Create two models with same random state
    model_dict = TabPFNRegressor(
        inference_config={"PREPROCESS_TRANSFORMS": [dict_config]},
        n_estimators=2,
        random_state=42,
    )

    model_obj = TabPFNRegressor(
        inference_config={"PREPROCESS_TRANSFORMS": [object_config]},
        n_estimators=2,
        random_state=42,
    )

    # Fit both models
    model_dict.fit(X, y)
    model_obj.fit(X, y)

    # Compare predictions for different output types
    for output_type in ["mean", "median", "mode"]:
        pred_dict = model_dict.predict(X, output_type=output_type)
        pred_obj = model_obj.predict(X, output_type=output_type)
        np.testing.assert_array_almost_equal(
            pred_dict,
            pred_obj,
            err_msg=f"Predictions differ for output_type={output_type}",
        )

    # Compare quantile predictions
    quantiles = [0.1, 0.5, 0.9]
    quant_dict = model_dict.predict(X, output_type="quantiles", quantiles=quantiles)
    quant_obj = model_obj.predict(X, output_type="quantiles", quantiles=quantiles)

    for q_dict, q_obj in zip(quant_dict, quant_obj):
        np.testing.assert_array_almost_equal(
            q_dict,
            q_obj,
            err_msg="Quantile predictions differ",
        )
