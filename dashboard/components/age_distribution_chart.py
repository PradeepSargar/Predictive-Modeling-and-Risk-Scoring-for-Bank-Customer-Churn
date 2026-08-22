from utils.chart_style import PLOTLY_CONFIG
# =============================================================================
# AGE DISTRIBUTION CHART
# =============================================================================

import streamlit as st
from utils.chart_factory import create_histogram
from utils.formatters import format_decimal


def display_age_distribution_chart(df, key: str = None):
    """
    Display customer age distribution histogram and clean summary statistics.
    """
    fig = create_histogram(
        data=df,
        x="Age",
        title="Customer Age Distribution",
        x_title="Age (Years)",
        y_title="Number of Customers",
        nbins=25,
        hovertemplate="<b>Age</b>: %{x} yrs<br>Customers: <b>%{y:,}</b><extra></extra>",
    )
    st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG, key=key)

    average_age = float(df["Age"].mean())
    minimum_age = int(df["Age"].min())
    maximum_age = int(df["Age"].max())
    median_age = float(df["Age"].median())

    st.markdown(
        f"""
        <div style="display:grid; grid-template-columns: repeat(4, 1fr); gap:0.45rem; margin-top:0.4rem; margin-bottom:0.85rem;">
            <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:10px; padding:0.5rem 0.6rem; text-align:center; box-shadow:0 1px 4px rgba(0,0,0,0.02);">
                <div style="font-size:0.68rem; color:#64748B; font-weight:700; text-transform:uppercase;">Average</div>
                <div style="font-size:0.96rem; font-weight:800; color:#0F172A; margin-top:0.1rem;">{format_decimal(average_age)} Yrs</div>
            </div>
            <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:10px; padding:0.5rem 0.6rem; text-align:center; box-shadow:0 1px 4px rgba(0,0,0,0.02);">
                <div style="font-size:0.68rem; color:#64748B; font-weight:700; text-transform:uppercase;">Median</div>
                <div style="font-size:0.96rem; font-weight:800; color:#0F172A; margin-top:0.1rem;">{format_decimal(median_age, 0)} Yrs</div>
            </div>
            <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:10px; padding:0.5rem 0.6rem; text-align:center; box-shadow:0 1px 4px rgba(0,0,0,0.02);">
                <div style="font-size:0.68rem; color:#64748B; font-weight:700; text-transform:uppercase;">Youngest</div>
                <div style="font-size:0.96rem; font-weight:800; color:#059669; margin-top:0.1rem;">{minimum_age} Yrs</div>
            </div>
            <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:10px; padding:0.5rem 0.6rem; text-align:center; box-shadow:0 1px 4px rgba(0,0,0,0.02);">
                <div style="font-size:0.68rem; color:#64748B; font-weight:700; text-transform:uppercase;">Oldest</div>
                <div style="font-size:0.96rem; font-weight:800; color:#0284C7; margin-top:0.1rem;">{maximum_age} Yrs</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )