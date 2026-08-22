# =============================================================================
# DATA SERVICE
# =============================================================================

"""
Loads and caches datasets used across the Bank Churn Intelligence Dashboard.
"""

from pathlib import Path
import pandas as pd
import streamlit as st

# =============================================================================
# Project Paths
# =============================================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "Raw"
    / "European_Bank.csv"
)

PROCESSED_DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "Processed"
    / "customer_risk_report.csv"
)


class DataService:

    @staticmethod
    @st.cache_data(show_spinner=False)
    def load_dataset() -> pd.DataFrame:
        """
        Load processed or raw European Bank customer dataset with caching.
        """
        if PROCESSED_DATA_PATH.exists():
            return pd.read_csv(PROCESSED_DATA_PATH)

        if RAW_DATA_PATH.exists():
            return pd.read_csv(RAW_DATA_PATH)

        raise FileNotFoundError(
            f"Dataset not found at either {PROCESSED_DATA_PATH} or {RAW_DATA_PATH}"
        )

    @staticmethod
    def get_cohort_summary(df: pd.DataFrame) -> dict:
        """
        Return pre-calculated metrics for the customer dataset.
        """
        total = len(df)
        churn_col = "Exited" if "Exited" in df.columns else ("exited" if "exited" in df.columns else None)
        churned = int(df[churn_col].sum()) if churn_col else 0
        churn_rate = (churned / total * 100) if total > 0 else 0.0

        active_col = "IsActiveMember" if "IsActiveMember" in df.columns else None
        active_count = int(df[active_col].sum()) if active_col else 0

        return {
            "total_customers": total,
            "churned_customers": churned,
            "retained_customers": total - churned,
            "churn_rate": churn_rate,
            "active_customers": active_count,
            "inactive_customers": total - active_count,
            "average_balance": float(df["Balance"].mean()) if "Balance" in df.columns else 0.0,
            "average_credit_score": float(df["CreditScore"].mean()) if "CreditScore" in df.columns else 0.0,
            "average_age": float(df["Age"].mean()) if "Age" in df.columns else 0.0,
        }