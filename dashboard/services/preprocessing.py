import pandas as pd
import numpy as np
from typing import Any, Optional

try:
    from utils.validation import (
        EXPECTED_FEATURES,
        validate_dataframe_structure,
        safe_enforce_column_order,
    )
except ImportError:
    from dashboard.utils.validation import (
        EXPECTED_FEATURES,
        validate_dataframe_structure,
        safe_enforce_column_order,
    )


class PreprocessingError(Exception):
    pass


def preprocess_customer_data(
    customer_data: pd.DataFrame,
    scaler: Optional[Any] = None,
    scale_features: bool = False,
) -> pd.DataFrame:
    """
    Standardize, encode, range-clamp, and optionally scale customer features for model inference.
    For Tree-based models (GradientBoosting, RandomForest, DecisionTree), scale_features=False preserves
    the exact natural feature thresholds used during training.
    """
    if customer_data is None:
        raise PreprocessingError("customer_data is None")

    if not isinstance(customer_data, pd.DataFrame):
        raise PreprocessingError(
            f"customer_data must be pandas DataFrame, got {type(customer_data).__name__}"
        )

    df = customer_data.copy()

    # Normalize categorical columns if present in string format
    if "Gender" in df.columns and (df["Gender"].dtype == object or pd.api.types.is_string_dtype(df["Gender"])):
        df["Gender"] = df["Gender"].apply(
            lambda x: 1 if str(x).lower().strip() in ("male", "1") else 0
        )

    if "Geography" in df.columns:
        if "Geography_Germany" not in df.columns:
            df["Geography_Germany"] = (df["Geography"].astype(str).str.strip() == "Germany").astype(int)
        if "Geography_Spain" not in df.columns:
            df["Geography_Spain"] = (df["Geography"].astype(str).str.strip() == "Spain").astype(int)
        df = df.drop(columns=["Geography"], errors="ignore")

    # Enforce expected features and column order
    df = safe_enforce_column_order(df)

    # Cast all columns to float numeric
    try:
        for col in EXPECTED_FEATURES:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0)
    except Exception as exc:
        raise PreprocessingError(f"Failed to coerce numeric values: {exc}") from exc

    # Clean NaN/Inf values
    try:
        df = df.replace([np.inf, -np.inf], np.nan)
        for col in EXPECTED_FEATURES:
            if df[col].isnull().any():
                df[col] = df[col].fillna(0.0)
    except Exception as exc:
        raise PreprocessingError(f"Failed to clean NaN/Inf values: {exc}") from exc

    # Range clamping
    try:
        clamp_ranges = {
            "CreditScore": (300.0, 900.0),
            "Age": (18.0, 100.0),
            "Tenure": (0.0, 10.0),
            "NumOfProducts": (1.0, 4.0),
            "HasCrCard": (0.0, 1.0),
            "IsActiveMember": (0.0, 1.0),
            "Balance": (0.0, 1e12),
            "EstimatedSalary": (0.0, 1e12),
            "Gender": (0.0, 1.0),
            "Geography_Germany": (0.0, 1.0),
            "Geography_Spain": (0.0, 1.0),
        }
        for col, (lo, hi) in clamp_ranges.items():
            if col in df.columns:
                df[col] = df[col].astype(float).clip(lower=lo, upper=hi)
    except Exception as exc:
        raise PreprocessingError(f"Failed to clamp ranges: {exc}") from exc

    # Validate structure
    columns_ok, col_msg = validate_dataframe_structure(df)
    if not columns_ok:
        raise PreprocessingError(f"DataFrame structure invalid: {col_msg}")

    # Scale numeric features only if explicitly requested (e.g. for Logistic Regression)
    if scale_features and scaler is not None:
        if not hasattr(scaler, "transform"):
            raise PreprocessingError("Scaler object does not have a 'transform' method")
        try:
            scaled_values = scaler.transform(df)
        except Exception as exc:
            raise PreprocessingError(f"Scaler.transform failed: {exc}") from exc

        if scaled_values is None:
            raise PreprocessingError("Scaler returned None")

        try:
            df = pd.DataFrame(
                scaled_values,
                columns=df.columns.tolist(),
                index=df.index,
            )
        except Exception as exc:
            raise PreprocessingError(f"Failed to reconstruct DataFrame after scaling: {exc}") from exc

    return df
