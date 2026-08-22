from utils.chart_style import PLOTLY_CONFIG
# =============================================================================
# PRODUCTS VS CHURN CHART
# =============================================================================

import streamlit as st
from utils.comparison_factory import create_comparison_chart
from utils.business_insights import generate_top_category_insight


def display_products_vs_churn_chart(df, key: str = None):
    """
    Display product holdings count vs customer churn breakdown.
    """
    prod_df = df.copy()
    prod_df["NumOfProducts"] = prod_df["NumOfProducts"].apply(lambda x: f"{x} Product{'s' if x != 1 else ''}")

    fig = create_comparison_chart(
        df=prod_df,
        category_column="NumOfProducts",
        target_column="Exited",
        chart_title="Customer Churn by Number of Products Held",
        x_title="Products Held",
        y_title="Number of Customers",
    )
    st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG, key=key)

    generate_top_category_insight(
        df=prod_df,
        category_column="NumOfProducts",
        target_column="Exited",
        positive_label="Churned Customers",
    )