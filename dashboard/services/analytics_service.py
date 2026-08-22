# =============================================================================
# ANALYTICS SERVICE
# =============================================================================

"""
Business Analytics Service

This module contains reusable analytics functions
used throughout the dashboard.
"""

import pandas as pd


class AnalyticsService:

    # ============================================================
    # Numeric Summary
    # ============================================================

    @staticmethod
    def numeric_summary(df, column):

        return {

            "mean": df[column].mean(),

            "median": df[column].median(),

            "min": df[column].min(),

            "max": df[column].max(),

            "std": df[column].std(),

            "count": df[column].count()

        }

    # ============================================================
    # Category Summary
    # ============================================================

    @staticmethod
    def category_summary(df, column):

        return (

            df[column]

            .value_counts()

            .reset_index()

        )

    # ============================================================
    # Churn Summary
    # ============================================================

    @staticmethod
    def churn_summary(df):

        total = len(df)

        churned = df["Exited"].sum()

        retained = total - churned

        churn_rate = (churned / total) * 100

        return {

            "total": total,

            "retained": retained,

            "churned": churned,

            "churn_rate": churn_rate

        }

    # ============================================================
    # Top Category
    # ============================================================

    @staticmethod
    def top_category(

        df,

        category_column,

        target_column

    ):

        result = (

            df[df[target_column] == 1]

            .groupby(category_column)

            .size()

            .sort_values(

                ascending=False

            )

        )

        return {

            "category": result.index[0],

            "count": result.iloc[0]

        }