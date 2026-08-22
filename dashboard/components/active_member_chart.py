from utils.chart_style import PLOTLY_CONFIG
# =============================================================================
# ACTIVE VS INACTIVE CUSTOMERS CHART
# =============================================================================

import streamlit as st
from utils.chart_factory import create_bar_chart
from utils.constants import SUCCESS_GREEN, DANGER_RED


def display_active_member_chart(df, key: str = None):
    """
    Display active vs inactive customer distribution.
    """
    activity_counts = (
        df["IsActiveMember"]
        .value_counts()
        .sort_index()
        .reset_index()
    )
    activity_counts.columns = ["Status", "Customers"]
    activity_counts["Status"] = activity_counts["Status"].replace({
        0: "Inactive",
        1: "Active",
    })

    fig = create_bar_chart(
        data=activity_counts,
        x="Status",
        y="Customers",
        color="Status",
        text="Customers",
        title="Customer Engagement Status",
        x_title="Membership Status",
        y_title="Number of Customers",
        color_discrete_map={
            "Inactive": DANGER_RED,
            "Active": SUCCESS_GREEN,
        },
        hovertemplate="<b>%{x}</b><br>Customers: <b>%{y:,}</b><extra></extra>",
    )

    st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG, key=key)