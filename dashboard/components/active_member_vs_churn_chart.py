from utils.chart_style import PLOTLY_CONFIG
# =============================================================================
# ACTIVE MEMBER VS CHURN CHART
# =============================================================================

import streamlit as st
from utils.comparison_factory import create_comparison_chart
from utils.business_insights import generate_top_category_insight


def display_active_member_vs_churn_chart(df, key: str = None):
    """
    Display active vs inactive customer churn comparison.
    """
    member_df = df.copy()
    member_df["IsActiveMember"] = member_df["IsActiveMember"].replace({
        0: "Inactive Member",
        1: "Active Member",
    })

    fig = create_comparison_chart(
        df=member_df,
        category_column="IsActiveMember",
        target_column="Exited",
        chart_title="Customer Churn by Membership Activity",
        x_title="Membership Status",
        y_title="Number of Customers",
    )
    st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG, key=key)

    generate_top_category_insight(
        df=member_df,
        category_column="IsActiveMember",
        target_column="Exited",
        positive_label="Churned Customers",
    )