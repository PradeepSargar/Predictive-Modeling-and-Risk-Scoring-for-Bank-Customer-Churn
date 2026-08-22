from utils.chart_style import PLOTLY_CONFIG
# =============================================================================
# ESTIMATED SALARY DISTRIBUTION CHART
# =============================================================================

import streamlit as st
from services.analytics_service import AnalyticsService
from utils.chart_factory import create_histogram
from utils.formatters import format_currency


def display_salary_distribution_chart(df, key: str = None):
    """
    Display estimated salary distribution and clean summary statistics.
    """
    fig = create_histogram(
        data=df,
        x="EstimatedSalary",
        title="Estimated Annual Salary Distribution",
        x_title="Estimated Salary ($)",
        y_title="Number of Customers",
        nbins=40,
        hovertemplate="<b>Salary</b>: %{x}<br>Customers: <b>%{y:,}</b><extra></extra>",
    )
    st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG, key=key)

    stats = AnalyticsService.numeric_summary(df, "EstimatedSalary")

    st.markdown(
        f"""
        <div style="display:grid; grid-template-columns: repeat(4, 1fr); gap:0.45rem; margin-top:0.4rem; margin-bottom:0.85rem;">
            <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:10px; padding:0.5rem 0.6rem; text-align:center; box-shadow:0 1px 4px rgba(0,0,0,0.02);">
                <div style="font-size:0.68rem; color:#64748B; font-weight:700; text-transform:uppercase;">Average</div>
                <div style="font-size:0.96rem; font-weight:800; color:#0F172A; margin-top:0.1rem;">{format_currency(stats['mean'])}</div>
            </div>
            <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:10px; padding:0.5rem 0.6rem; text-align:center; box-shadow:0 1px 4px rgba(0,0,0,0.02);">
                <div style="font-size:0.68rem; color:#64748B; font-weight:700; text-transform:uppercase;">Median</div>
                <div style="font-size:0.96rem; font-weight:800; color:#0F172A; margin-top:0.1rem;">{format_currency(stats['median'])}</div>
            </div>
            <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:10px; padding:0.5rem 0.6rem; text-align:center; box-shadow:0 1px 4px rgba(0,0,0,0.02);">
                <div style="font-size:0.68rem; color:#64748B; font-weight:700; text-transform:uppercase;">Max Salary</div>
                <div style="font-size:0.96rem; font-weight:800; color:#059669; margin-top:0.1rem;">{format_currency(stats['max'])}</div>
            </div>
            <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:10px; padding:0.5rem 0.6rem; text-align:center; box-shadow:0 1px 4px rgba(0,0,0,0.02);">
                <div style="font-size:0.68rem; color:#64748B; font-weight:700; text-transform:uppercase;">Min Salary</div>
                <div style="font-size:0.96rem; font-weight:800; color:#64748B; margin-top:0.1rem;">{format_currency(stats['min'])}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )