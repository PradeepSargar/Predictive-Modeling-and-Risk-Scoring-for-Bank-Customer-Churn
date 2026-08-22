# =============================================================================
# EXECUTIVE SERVICE
# =============================================================================

"""
Provides business metrics for the Executive Dashboard.
"""

# =============================================================================
# Import Required Libraries
# =============================================================================

import pandas as pd


class ExecutiveService:

    # ============================================================
    # Dataset Summary
    # ============================================================

    @staticmethod
    def dataset_summary(df: pd.DataFrame):

        total_customers = len(df)

        active_customers = int(

            df["IsActiveMember"].sum()

        )

        inactive_customers = total_customers - active_customers

        churn_rate = round(

            df["Exited"].mean() * 100,

            2

        )

        average_balance = round(

            df["Balance"].mean(),

            2

        )

        average_credit_score = round(

            df["CreditScore"].mean(),

            2

        )

        average_age = round(

            df["Age"].mean(),

            2

        )

        total_features = len(

            df.columns

        )

        return {

            # ====================================================
            # Dataset Information
            # ====================================================

            "total_customers": total_customers,

            "total_features": total_features,

            # ====================================================
            # Customer Statistics
            # ====================================================

            "active_customers": active_customers,

            "inactive_customers": inactive_customers,

            "churn_rate": churn_rate,

            # ====================================================
            # Business KPIs
            # ====================================================

            "average_balance": average_balance,

            "average_credit_score": average_credit_score,

            "average_age": average_age,

            # ====================================================
            # Backward Compatibility
            # ====================================================

            "customers": total_customers,

            "features": total_features

        }
    