import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple, Optional

EXPECTED_FEATURES = [
    "CreditScore",
    "Gender",
    "Age",
    "Tenure",
    "Balance",
    "NumOfProducts",
    "HasCrCard",
    "IsActiveMember",
    "EstimatedSalary",
    "Geography_Germany",
    "Geography_Spain",
]

VALID_RANGES = {
    "CreditScore": (300, 900),
    "Age": (18, 100),
    "Tenure": (0, 10),
    "Balance": (0.0, 1_000_000.0),
    "NumOfProducts": (1, 4),
    "HasCrCard": (0, 1),
    "IsActiveMember": (0, 1),
    "EstimatedSalary": (0.0, 10_000_000.0),
    "Gender": (0, 1),
    "Geography_Germany": (0, 1),
    "Geography_Spain": (0, 1),
}


class ValidationError(Exception):
    pass


def validate_customer_params(params: Dict[str, Any]) -> Tuple[bool, str]:
    if not isinstance(params, dict):
        return False, "Parameters must be a dictionary"

    required_keys = [
        "CreditScore", "Gender", "Age", "Tenure", "Balance",
        "NumOfProducts", "HasCrCard", "IsActiveMember",
        "EstimatedSalary", "Geography"
    ]
    missing = [k for k in required_keys if k not in params]
    if missing:
        return False, f"Missing required fields: {', '.join(missing)}"

    cs = params.get("CreditScore")
    if not isinstance(cs, (int, float)) or not (VALID_RANGES["CreditScore"][0] <= cs <= VALID_RANGES["CreditScore"][1]):
        return False, f"CreditScore must be between {VALID_RANGES['CreditScore'][0]} and {VALID_RANGES['CreditScore'][1]}"

    age = params.get("Age")
    if not isinstance(age, (int, float)) or not (VALID_RANGES["Age"][0] <= age <= VALID_RANGES["Age"][1]):
        return False, f"Age must be between {VALID_RANGES['Age'][0]} and {VALID_RANGES['Age'][1]}"

    tenure = params.get("Tenure")
    if not isinstance(tenure, (int, float)) or not (VALID_RANGES["Tenure"][0] <= tenure <= VALID_RANGES["Tenure"][1]):
        return False, f"Tenure must be between {VALID_RANGES['Tenure'][0]} and {VALID_RANGES['Tenure'][1]}"

    balance = params.get("Balance")
    if not isinstance(balance, (int, float)) or balance < VALID_RANGES["Balance"][0]:
        return False, f"Balance must be >= ${VALID_RANGES['Balance'][0]:,.0f}"

    salary = params.get("EstimatedSalary")
    if not isinstance(salary, (int, float)) or salary < VALID_RANGES["EstimatedSalary"][0]:
        return False, f"EstimatedSalary must be >= ${VALID_RANGES['EstimatedSalary'][0]:,.0f}"

    products = params.get("NumOfProducts")
    if products not in (1, 2, 3, 4):
        return False, "NumOfProducts must be one of 1, 2, 3, 4"

    if params.get("HasCrCard") not in (0, 1):
        return False, "HasCrCard must be 0 or 1"

    if params.get("IsActiveMember") not in (0, 1):
        return False, "IsActiveMember must be 0 or 1"

    if params.get("Gender") not in ("Male", "Female", 0, 1):
        return False, "Gender must be 'Male' or 'Female' (or 0/1)"

    if params.get("Geography") not in ("France", "Germany", "Spain"):
        return False, "Geography must be 'France', 'Germany', or 'Spain'"

    return True, "OK"


def validate_dataframe_structure(df: pd.DataFrame) -> Tuple[bool, str]:
    if not isinstance(df, pd.DataFrame):
        return False, "Input must be a pandas DataFrame"

    if df.empty:
        return False, "DataFrame is empty"

    if df.shape[0] == 0:
        return False, "DataFrame has no rows"

    for col in EXPECTED_FEATURES:
        if col not in df.columns:
            return False, f"Missing expected column: {col}"

    extra_cols = [c for c in df.columns if c not in EXPECTED_FEATURES]
    if extra_cols:
        return False, f"Unexpected columns: {', '.join(extra_cols)}"

    if df.columns.tolist() != EXPECTED_FEATURES:
        return False, "Column order does not match expected feature order"

    for col in EXPECTED_FEATURES:
        if df[col].isnull().any():
            return False, f"Column '{col}' contains null/NaN values"
        if pd.api.types.is_numeric_dtype(df[col]):
            numeric_vals = pd.to_numeric(df[col], errors="coerce").fillna(0).to_numpy()
            if np.isinf(numeric_vals).any():
                return False, f"Column '{col}' contains infinite values"

    for col, (lo, hi) in VALID_RANGES.items():
        if col in df.columns:
            series = pd.to_numeric(df[col], errors="coerce").fillna(0)
            if ((series < lo) | (series > hi)).any():
                return False, f"Column '{col}' has values outside valid range [{lo}, {hi}]"

    return True, "DataFrame structure OK"


def safe_enforce_column_order(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for col in EXPECTED_FEATURES:
        if col not in df.columns:
            df[col] = 0
    return df[EXPECTED_FEATURES].copy()


def sanitize_probability(p: float) -> float:
    if p is None:
        return 0.0
    try:
        p = float(p)
    except (TypeError, ValueError):
        return 0.0
    if np.isnan(p) or np.isinf(p):
        return 0.0
    return max(0.0, min(1.0, p))


def compute_safe_delta(baseline_proba: float, scenario_proba: float) -> Tuple[float, float]:
    bp = sanitize_probability(baseline_proba)
    sp = sanitize_probability(scenario_proba)
    delta_abs = sp - bp
    if abs(bp) < 1e-9:
        delta_pct = 0.0 if abs(delta_abs) < 1e-9 else (100.0 if delta_abs > 0 else -100.0)
    else:
        delta_pct = (delta_abs / bp) * 100.0
    delta_pct = max(-10_000.0, min(10_000.0, delta_pct))
    return delta_abs, delta_pct
