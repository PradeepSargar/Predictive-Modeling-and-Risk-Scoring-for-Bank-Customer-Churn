# =============================================================================
# CHURN DISTRIBUTION DONUT CHART
# =============================================================================

"""
Displays the overall churn distribution of the customer cohort.
"""

import plotly.express as px
import streamlit as st
from utils.constants import PRIMARY_BLUE, DANGER_RED
from utils.chart_style import PLOTLY_CONFIG, apply_dashboard_style


def display_churn_distribution_chart(df, key: str = None):
    """
    Display a styled donut chart showing Retained vs Churned proportions.
    """
    churn_col = "Exited" if "Exited" in df.columns else ("exited" if "exited" in df.columns else None)
    churned = int(df[churn_col].sum()) if churn_col else 0
    retained = len(df) - churned

    chart_data = {
        "Status": ["Retained Customers", "Churned Customers"],
        "Customers": [retained, churned],
    }

    fig = px.pie(
        chart_data,
        names="Status",
        values="Customers",
        hole=0.55,
        color="Status",
        color_discrete_map={
            "Retained Customers": PRIMARY_BLUE,
            "Churned Customers": DANGER_RED,
        },
    )

    fig = apply_dashboard_style(
        fig=fig,
        title="Portfolio Churn Breakdown",
        x_title="",
        y_title="",
        height=380,
        showlegend=True,
    )

    st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG, key=key)