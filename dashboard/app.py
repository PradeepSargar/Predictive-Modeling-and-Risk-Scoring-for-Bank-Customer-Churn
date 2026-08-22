import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import pandas as pd

from components.theme import apply_global_theme
from components.sidebar import display_sidebar
from components.header import display_brand_header
from components.section_header import display_section_header

from services.data_service import DataService
from services.executive_service import ExecutiveService

from components.executive_kpi_cards import display_executive_kpi_cards
from components.customer_status_chart import display_customer_status_chart
from components.churn_distribution_chart import display_churn_distribution_chart
from components.model_performance_cards import display_model_performance_cards
from components.executive_recommendations import display_executive_recommendations
from utils.helpers import init_session_state_defaults, render_error_banner


def render_raw_html(html_str: str):
    """
    Safely render raw HTML directly into the DOM without CommonMark code-block conversion.
    """
    if hasattr(st, "html"):
        st.html(html_str)
    else:
        clean_html = "".join(line.strip() for line in html_str.splitlines() if line.strip())
        st.markdown(clean_html, unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# Streamlit Application Configuration
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Bank Churn Intelligence | Executive Risk Platform",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_global_theme()
init_session_state_defaults()
display_sidebar()

# -----------------------------------------------------------------------------
# Brand Hero Header
# -----------------------------------------------------------------------------
display_brand_header(
    title="Bank Customer Churn Intelligence",
    subtitle="Enterprise Predictive Modeling, Risk Scoring & Explainable AI Retention Platform",
    badges=[
        ("🏆", "Champion: Gradient Boosting"),
        ("🎯", "86.31% CV Accuracy"),
        ("📈", "86.48% CV ROC-AUC"),
        ("🔮", "Live Scoring Engine"),
    ],
    icon="🏦",
)

try:
    df = DataService.load_dataset()
except Exception as error:
    render_error_banner(
        title="Unable to Load Customer Dataset",
        detail=str(error),
        suggestion="Verify that European_Bank.csv exists in /data/Raw/ or customer_risk_report.csv in /data/Processed/.",
    )
    st.stop()

summary = ExecutiveService.dataset_summary(df)

# Top Executive KPI Grid
display_executive_kpi_cards(summary)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# Customer Health & Attrition Distribution
display_section_header(
    "Portfolio Health & Risk Distribution",
    "Customer engagement status and overall portfolio churn proportion at a glance.",
    accent_color="#0EA5E9",
)

col1, col2 = st.columns(2, gap="medium")
with col1:
    display_customer_status_chart(df)

with col2:
    display_churn_distribution_chart(df)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# Strategic Executive Recommendations
display_section_header(
    "Strategic Executive Recommendations",
    "Tailored retention and portfolio growth priorities based on current cohort metrics.",
    accent_color="#A855F7",
)

display_executive_recommendations(summary)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# Champion Model Production Benchmark Summary
display_section_header(
    "Production Model Benchmark Summary",
    "Quarterly tracking metrics for the deployed Gradient Boosting champion model.",
    accent_color="#10B981",
)

display_model_performance_cards()

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# Quick Navigation Callout Grid
quick_nav_html = (
    "<div style='margin-top:0.5rem; padding:1.25rem 1.5rem; border-radius:14px; background:linear-gradient(135deg, #F0F9FF 0%, #FFFFFF 100%); border:1px solid #BAE6FD; box-shadow:0 4px 18px -2px rgba(14,165,233,0.06);'>"
    "<div style='font-weight:700; color:#0F172A; font-size:1.02rem; margin-bottom:0.6rem;'>🧭 Quick Platform Navigation</div>"
    "<div style='display:grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap:0.75rem;'>"
    "<div style='padding:0.75rem 0.9rem; background:#FFFFFF; border:1px solid #E2E8F0; border-radius:10px;'>"
    "<div style='font-weight:700; font-size:0.88rem; color:#0F172A;'>📊 02 Customer Analytics</div>"
    "<div style='font-size:0.78rem; color:#64748B; margin-top:0.2rem;'>Demographics, behavior, and churn breakdown across 4 tabs.</div>"
    "</div>"
    "<div style='padding:0.75rem 0.9rem; background:#FFFFFF; border:1px solid #E2E8F0; border-radius:10px;'>"
    "<div style='font-weight:700; font-size:0.88rem; color:#0F172A;'>🎯 03 Risk Portfolio</div>"
    "<div style='font-size:0.78rem; color:#64748B; margin-top:0.2rem;'>Multi-filter triage table to prioritize high-risk accounts.</div>"
    "</div>"
    "<div style='padding:0.75rem 0.9rem; background:#FFFFFF; border:1px solid #E2E8F0; border-radius:10px;'>"
    "<div style='font-weight:700; font-size:0.88rem; color:#0F172A;'>🏆 04 Model Performance</div>"
    "<div style='font-size:0.78rem; color:#64748B; margin-top:0.2rem;'>5-model benchmark comparison table and confusion matrix.</div>"
    "</div>"
    "<div style='padding:0.75rem 0.9rem; background:#FFFFFF; border:1px solid #E2E8F0; border-radius:10px;'>"
    "<div style='font-weight:700; font-size:0.88rem; color:#0F172A;'>🔮 06 Customer Risk Scoring</div>"
    "<div style='font-size:0.78rem; color:#64748B; margin-top:0.2rem;'>Real-time single customer intake and batch CSV scoring.</div>"
    "</div>"
    "</div>"
    "</div>"
)
render_raw_html(quick_nav_html)
