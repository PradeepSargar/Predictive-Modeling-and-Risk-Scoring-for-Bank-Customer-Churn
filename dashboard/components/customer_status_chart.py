# =============================================================================
# CUSTOMER STATUS DONUT CHART
# =============================================================================

"""
Displays the Active vs Inactive Customer Distribution.
"""

import plotly.express as px
import streamlit as st
from utils.constants import SUCCESS_GREEN, WARNING_AMBER
from utils.chart_style import PLOTLY_CONFIG, apply_dashboard_style


def display_customer_status_chart(df, key: str = None):
    """
    Display customer activity status donut chart.
    """
    active_col = "IsActiveMember" if "IsActiveMember" in df.columns else None
    active = int(df[active_col].sum()) if active_col else 0
    inactive = len(df) - active

    status_data = {
        "Customer Status": ["Active Members", "Inactive Members"],
        "Customers": [active, inactive],
    }

    fig = px.pie(
        status_data,
        names="Customer Status",
        values="Customers",
        hole=0.55,
        color="Customer Status",
        color_discrete_map={
            "Active Members": SUCCESS_GREEN,
            "Inactive Members": WARNING_AMBER,
        },
    )

    fig = apply_dashboard_style(
        fig=fig,
        title="Customer Engagement Split",
        x_title="",
        y_title="",
        height=380,
        showlegend=True,
    )

    st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG, key=key)