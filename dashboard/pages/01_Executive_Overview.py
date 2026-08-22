import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st

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
from utils.helpers import render_error_banner

st.set_page_config(
    page_title="Executive Overview | Bank Churn Intelligence",
    page_icon="👔",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_global_theme()
display_sidebar()

display_brand_header(
    title="Executive Overview",
    subtitle="High-level customer portfolio health, attrition benchmarks, and strategic growth priorities for executive leadership.",
    badges=[
        ("👔", "Executive View"),
        ("📊", "10,000 Accounts"),
        ("🧭", "Data-Driven Strategy"),
        ("🏆", "Gradient Boosting · 86.31% CV Acc"),
    ],
    icon="👔",
)

try:
    df = DataService.load_dataset()
except Exception as error:
    render_error_banner(
        title="Unable to Load Customer Dataset",
        detail=str(error),
        suggestion="Verify that European_Bank.csv exists in /data/Raw/ or customer_risk_report.csv exists in /data/Processed/.",
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

# Champion Model Production Benchmark Cards
display_section_header(
    "Production Model Benchmark Summary",
    "Quarterly tracking metrics for the deployed Gradient Boosting champion model.",
    accent_color="#10B981",
)

display_model_performance_cards()

st.markdown(
    """
    <div style="margin-top:1.5rem; padding:0.9rem 1.25rem; border-radius:14px; background:linear-gradient(135deg, #F0F9FF 0%, #FFFFFF 100%); border:1px solid #BAE6FD; text-align:center;">
        <div style="font-size:0.78rem; color:#0284C7; font-weight:600;">Bank Customer Churn Intelligence System · Executive Overview Report</div>
    </div>
    """,
    unsafe_allow_html=True,
)
