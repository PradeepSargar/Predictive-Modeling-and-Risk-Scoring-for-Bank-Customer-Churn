import streamlit as st

from components.kpi_card import render_kpi_row
from components.section_header import display_section_header


def display_executive_kpi_cards(summary):
    display_section_header(
        "Executive Business KPIs",
        "Real-time snapshot of customer portfolio health and key operational metrics.",
        accent_color="#1E40AF",
    )

    row1 = [
        {"title": "Total Customers", "value": f"{summary.get('customers', summary.get('total_customers', 10000)):,}",
         "icon": "👥", "variant": "blue",
         "subtitle": "Full portfolio size"},
        {"title": "Portfolio Churn Rate", "value": f"{summary.get('churn_rate', 20.37)}%",
         "icon": "📉", "variant": "red",
         "subtitle": "Customer attrition rate",
         "delta": "1.2%", "delta_positive": False},
        {"title": "Active Members", "value": f"{summary.get('active_customers', 5151):,}",
         "icon": "🟢", "variant": "green",
         "subtitle": "Engaged customers"},
        {"title": "Inactive Members", "value": f"{summary.get('inactive_customers', 4849):,}",
         "icon": "⚪", "variant": "amber",
         "subtitle": "Retention candidates"},
    ]
    render_kpi_row(row1, cols=4)

    st.markdown('<div style="height:0.25rem;"></div>', unsafe_allow_html=True)

    avg_bal = summary.get("average_balance", 76485.89)
    avg_cs = summary.get("average_credit_score", 650.53)
    avg_age = summary.get("average_age", 38.92)

    row2 = [
        {"title": "Avg. Customer Balance", "value": f"${avg_bal:,.2f}",
         "icon": "💰", "variant": "green",
         "subtitle": "Mean deposit per customer"},
        {"title": "Avg. Credit Score", "value": f"{avg_cs:,.0f}",
         "icon": "⭐", "variant": "purple",
         "subtitle": "Cohort credit quality"},
        {"title": "Avg. Customer Age", "value": f"{avg_age:.1f} yrs",
         "icon": "🎂", "variant": "amber",
         "subtitle": "Portfolio age profile"},
        {"title": "Production Model", "value": "Gradient Boosting",
         "icon": "🏆", "variant": "blue",
         "subtitle": "Champion · 86.31% CV Acc"},
    ]
    render_kpi_row(row2, cols=4)
