import pandas as pd
import numpy as np
from typing import Any, Tuple, Optional

try:
    from services.preprocessing import preprocess_customer_data
    from utils.constants import (
        LOW_RISK_THRESHOLD,
        MEDIUM_RISK_THRESHOLD,
        LOW_RISK,
        MEDIUM_RISK,
        HIGH_RISK,
        CHURN,
        NO_CHURN,
    )
    from utils.validation import sanitize_probability, safe_enforce_column_order
except ImportError:
    from dashboard.services.preprocessing import preprocess_customer_data
    from dashboard.utils.constants import (
        LOW_RISK_THRESHOLD,
        MEDIUM_RISK_THRESHOLD,
        LOW_RISK,
        MEDIUM_RISK,
        HIGH_RISK,
        CHURN,
        NO_CHURN,
    )
    from dashboard.utils.validation import sanitize_probability, safe_enforce_column_order


class PredictionError(Exception):
    pass


def predict_customer(
    customer_data: pd.DataFrame,
    gradient_boosting_model: Any,
    scaler: Optional[Any] = None,
    decision_threshold: float = 0.50,
) -> Tuple[int, str, float, str]:
    """
    Score a single customer DataFrame and return (prediction, label, probability, risk_tier).
    Preserves raw feature thresholds for Gradient Boosting production classifier.
    Supports flexible decision_threshold for policy tuning (e.g. 0.35 optimal retention).
    """
    if gradient_boosting_model is None:
        raise PredictionError("Gradient Boosting model is None — cannot predict")

    if not hasattr(gradient_boosting_model, "predict"):
        raise PredictionError("Model missing 'predict' method — invalid model object")

    if not hasattr(gradient_boosting_model, "predict_proba"):
        raise PredictionError("Model missing 'predict_proba' method — invalid model object")

    try:
        # Gradient Boosting was trained on unscaled features
        processed_data = preprocess_customer_data(customer_data, scaler=scaler, scale_features=False)
    except Exception as exc:
        raise PredictionError(f"Preprocessing failed: {exc}") from exc

    if processed_data is None or processed_data.shape[0] == 0:
        raise PredictionError("No data rows available after preprocessing")

    try:
        proba_array = gradient_boosting_model.predict_proba(processed_data)
    except Exception as exc:
        raise PredictionError(f"Model.predict_proba() failed: {exc}") from exc

    if proba_array is None or len(proba_array) == 0:
        raise PredictionError("Model.predict_proba() returned empty result")

    proba_shape = proba_array[0] if hasattr(proba_array[0], "__len__") else [proba_array[0]]
    if len(proba_shape) >= 2:
        probability_raw = float(proba_array[0][1])
    else:
        probability_raw = float(proba_array[0][0])

    probability = sanitize_probability(probability_raw)

    # Dynamic decision thresholding for binary classification
    prediction = 1 if probability >= decision_threshold else 0

    if probability < LOW_RISK_THRESHOLD:
        risk_level = LOW_RISK
    elif probability < MEDIUM_RISK_THRESHOLD:
        risk_level = MEDIUM_RISK
    else:
        risk_level = HIGH_RISK

    prediction_label = CHURN if prediction == 1 else NO_CHURN

    return prediction, prediction_label, probability, risk_level


def predict_batch(
    customers_df: pd.DataFrame,
    gradient_boosting_model: Any,
    scaler: Optional[Any] = None,
    decision_threshold: float = 0.50,
) -> pd.DataFrame:
    """
    Score a batch DataFrame of customer records and append prediction columns.
    Supports flexible decision_threshold for policy tuning (e.g. 0.35 optimal retention).
    """
    if gradient_boosting_model is None:
        raise PredictionError("Model is not loaded.")

    df_out = customers_df.copy()

    # Normalize categorical columns if present in raw string format
    model_input = customers_df.copy()
    if "Gender" in model_input.columns and (model_input["Gender"].dtype == object or pd.api.types.is_string_dtype(model_input["Gender"])):
        model_input["Gender"] = model_input["Gender"].apply(
            lambda x: 1 if str(x).lower().strip() in ("male", "1") else 0
        )

    if "Geography" in model_input.columns:
        if "Geography_Germany" not in model_input.columns:
            model_input["Geography_Germany"] = (model_input["Geography"].astype(str).str.strip() == "Germany").astype(int)
        if "Geography_Spain" not in model_input.columns:
            model_input["Geography_Spain"] = (model_input["Geography"].astype(str).str.strip() == "Spain").astype(int)
        model_input = model_input.drop(columns=["Geography"], errors="ignore")

    # Enforce exact model columns and order
    model_input = safe_enforce_column_order(model_input)
    processed = preprocess_customer_data(model_input, scaler=scaler, scale_features=False)

    probabilities = gradient_boosting_model.predict_proba(processed)[:, 1]
    predictions = (probabilities >= decision_threshold).astype(int)

    rounded_probas = np.round(probabilities, 4)
    df_out["Churn_Probability"] = rounded_probas
    df_out["Risk_Score"] = np.round(rounded_probas * 100.0, 1)
    df_out["Churn_Probability_Pct"] = (rounded_probas * 100).round(1).astype(str) + "%"
    df_out["Predicted_Status"] = [CHURN if p == 1 else NO_CHURN for p in predictions]
    df_out["Risk_Tier"] = [
        LOW_RISK if p < LOW_RISK_THRESHOLD else (MEDIUM_RISK if p < MEDIUM_RISK_THRESHOLD else HIGH_RISK)
        for p in rounded_probas
    ]

    return df_out
