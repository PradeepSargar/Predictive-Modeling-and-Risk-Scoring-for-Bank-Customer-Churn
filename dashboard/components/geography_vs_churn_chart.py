from utils.chart_style import PLOTLY_CONFIG
# =============================================================================
# GEOGRAPHY VS CHURN CHART
# =============================================================================

import streamlit as st
from utils.comparison_factory import create_comparison_chart
from utils.business_insights import generate_top_category_insight


def display_geography_vs_churn_chart(df, key: str = None):
    """
    Display geography vs customer churn comparison.
    """
    fig = create_comparison_chart(
        df=df,
        category_column="Geography",
        target_column="Exited",
        chart_title="Customer Churn by Geography",
        x_title="Country",
        y_title="Number of Customers",
    )
    st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG, key=key)

    generate_top_category_insight(
        df=df,
        category_column="Geography",
        target_column="Exited",
        positive_label="Churned Customers",
    )