from utils.chart_style import PLOTLY_CONFIG
# =============================================================================
# CREDIT SCORE DISTRIBUTION CHART
# =============================================================================

import streamlit as st
from utils.chart_factory import create_histogram
from utils.formatters import format_decimal


def display_credit_score_distribution_chart(df, key: str = None):
    """
    Display credit score distribution and clean summary statistics.
    """
    fig = create_histogram(
        data=df,
        x="CreditScore",
        title="Customer Credit Score Distribution",
        x_title="Credit Score",
        y_title="Number of Customers",
        nbins=30,
        hovertemplate="<b>Credit Score</b>: %{x}<br>Customers: <b>%{y:,}</b><extra></extra>",
    )
    st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG, key=key)

    average_score = float(df["CreditScore"].mean())
    minimum_score = int(df["CreditScore"].min())
    maximum_score = int(df["CreditScore"].max())
    median_score = float(df["CreditScore"].median())

    st.markdown(
        f"""
        <div style="display:grid; grid-template-columns: repeat(4, 1fr); gap:0.45rem; margin-top:0.4rem; margin-bottom:0.85rem;">
            <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:10px; padding:0.5rem 0.6rem; text-align:center; box-shadow:0 1px 4px rgba(0,0,0,0.02);">
                <div style="font-size:0.68rem; color:#64748B; font-weight:700; text-transform:uppercase;">Average</div>
                <div style="font-size:0.96rem; font-weight:800; color:#0F172A; margin-top:0.1rem;">{format_decimal(average_score, 0)}</div>
            </div>
            <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:10px; padding:0.5rem 0.6rem; text-align:center; box-shadow:0 1px 4px rgba(0,0,0,0.02);">
                <div style="font-size:0.68rem; color:#64748B; font-weight:700; text-transform:uppercase;">Median</div>
                <div style="font-size:0.96rem; font-weight:800; color:#0F172A; margin-top:0.1rem;">{format_decimal(median_score, 0)}</div>
            </div>
            <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:10px; padding:0.5rem 0.6rem; text-align:center; box-shadow:0 1px 4px rgba(0,0,0,0.02);">
                <div style="font-size:0.68rem; color:#64748B; font-weight:700; text-transform:uppercase;">Highest</div>
                <div style="font-size:0.96rem; font-weight:800; color:#059669; margin-top:0.1rem;">{maximum_score}</div>
            </div>
            <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:10px; padding:0.5rem 0.6rem; text-align:center; box-shadow:0 1px 4px rgba(0,0,0,0.02);">
                <div style="font-size:0.68rem; color:#64748B; font-weight:700; text-transform:uppercase;">Lowest</div>
                <div style="font-size:0.96rem; font-weight:800; color:#EF4444; margin-top:0.1rem;">{minimum_score}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )