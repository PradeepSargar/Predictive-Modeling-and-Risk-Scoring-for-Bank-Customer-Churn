import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd

from components.theme import apply_global_theme
from components.sidebar import display_sidebar
from components.header import display_brand_header
from components.section_header import display_section_header
from components.kpi_card import render_kpi_row
from utils.helpers import init_session_state_defaults


def render_raw_html(html_str: str):
    """
    Safely render raw HTML directly into the DOM without CommonMark code-block conversion.
    """
    if hasattr(st, "html"):
        st.html(html_str)
    else:
        clean_html = "".join(line.strip() for line in html_str.splitlines() if line.strip())
        st.markdown(clean_html, unsafe_allow_html=True)


st.set_page_config(
    page_title="Platform Overview | Bank Churn Intelligence",
    page_icon="ℹ️",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_global_theme()
init_session_state_defaults()
display_sidebar()

display_brand_header(
    title="Platform Overview & Architecture",
    subtitle="Technical architecture, data lifecycle, machine learning pipeline, and explainability framework for enterprise retail banking.",
    badges=[
        ("🏦", "Enterprise Retail Banking"),
        ("⚡", "Real-Time Inference"),
        ("🧠", "Tree-SHAP Explainability"),
        ("🏆", "Gradient Boosting Champion"),
    ],
    icon="ℹ️",
)

# -----------------------------------------------------------------------------
# Section 1: Executive Purpose & Problem Statement
# -----------------------------------------------------------------------------
display_section_header(
    "Platform Purpose & Business Problem",
    "Understanding the business economics of retail banking customer retention.",
    accent_color="#0EA5E9",
)

overview_col1, overview_col2 = st.columns(2, gap="medium")

with overview_col1:
    card1_html = (
        "<div class='card-surface card-gradient-blue' style='height:100%;'>"
        "<div class='card-header'>"
        "<div class='card-icon card-icon-blue'>🎯</div>"
        "<div>"
        "<div class='card-title'>The Attrition Challenge</div>"
        "<h3 style='margin:0; font-size:1.05rem; color:#0F172A;'>Cost of Customer Attrition</h3>"
        "</div>"
        "</div>"
        "<p style='margin:0.75rem 0 0 0; font-size:0.88rem; color:#334155; line-height:1.65;'>"
        "In retail banking, acquiring a new customer costs <b>5× to 25× more</b> than retaining an existing account. "
        "When high-value deposit holders churn, the institution loses not only immediate fee and interest income, "
        "but also significant long-term Customer Lifetime Value (CLV). "
        "This platform shifts the banking team from reactive recovery to <b>predictive, pre-emptive retention</b>."
        "</p>"
        "</div>"
    )
    render_raw_html(card1_html)

with overview_col2:
    card2_html = (
        "<div class='card-surface card-gradient-green' style='height:100%;'>"
        "<div class='card-header'>"
        "<div class='card-icon card-icon-green'>💡</div>"
        "<div>"
        "<div class='card-title'>Enterprise Solution</div>"
        "<h3 style='margin:0; font-size:1.05rem; color:#0F172A;'>Predictive Risk Intelligence Engine</h3>"
        "</div>"
        "</div>"
        "<ul class='list-clean' style='margin-top:0.75rem;'>"
        "<li><span class='list-check'>✓</span><b>Continuous Probability Scoring</b>: Calibrated risk scores (0.0% to 100.0%)</li>"
        "<li><span class='list-check'>✓</span><b>Explainable AI Transparency</b>: Global feature rankings and local SHAP waterfalls</li>"
        "<li><span class='list-check'>✓</span><b>Portfolio-Wide Prioritization</b>: Filterable queue of high-balance at-risk accounts</li>"
        "<li><span class='list-check'>✓</span><b>Scenario Sandbox</b>: Test product bundling and engagement levers in real time</li>"
        "<li><span class='list-check'>✓</span><b>Actionable Playbooks</b>: SLA-governed operational intervention matrix</li>"
        "</ul>"
        "</div>"
    )
    render_raw_html(card2_html)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Section 2: Machine Learning Workflow & Architecture
# -----------------------------------------------------------------------------
display_section_header(
    "End-to-End Analytics & ML Lifecycle",
    "Systematic pipeline from raw ingestion to calibrated prediction and explainable attribution.",
    accent_color="#A855F7",
)

pipeline_html = (
    "<div class='card-surface' style='padding:1.25rem 1.4rem; margin-bottom:1.5rem;'>"
    "<div style='display:grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap:1rem;'>"
    "<div style='padding:0.85rem; border-radius:10px; background:#F8FAFC; border-left:3px solid #0EA5E9;'>"
    "<div style='font-weight:800; color:#0EA5E9; font-size:0.78rem; text-transform:uppercase;'>Phase 1</div>"
    "<div style='font-weight:700; color:#0F172A; font-size:0.92rem; margin:0.2rem 0;'>Data Ingestion</div>"
    "<div style='font-size:0.8rem; color:#64748B;'>10,000 retail accounts with demographics, balances, and product holdings.</div>"
    "</div>"
    "<div style='padding:0.85rem; border-radius:10px; background:#F8FAFC; border-left:3px solid #A855F7;'>"
    "<div style='font-weight:800; color:#A855F7; font-size:0.78rem; text-transform:uppercase;'>Phase 2</div>"
    "<div style='font-weight:700; color:#0F172A; font-size:0.92rem; margin:0.2rem 0;'>Feature Pipeline</div>"
    "<div style='font-size:0.8rem; color:#64748B;'>StandardScaler normalization, one-hot country flags, schema verification.</div>"
    "</div>"
    "<div style='padding:0.85rem; border-radius:10px; background:#F8FAFC; border-left:3px solid #10B981;'>"
    "<div style='font-weight:800; color:#10B981; font-size:0.78rem; text-transform:uppercase;'>Phase 3</div>"
    "<div style='font-weight:700; color:#0F172A; font-size:0.92rem; margin:0.2rem 0;'>Champion Ensemble</div>"
    "<div style='font-size:0.8rem; color:#64748B;'>5-model stratified cross-validation selecting Gradient Boosting (86.31% ± 0.99% CV accuracy, 86.48% ± 0.99% ROC-AUC) over XGBoost, Random Forest, Logistic Regression, and Decision Tree.</div>"
    "</div>"
    "<div style='padding:0.85rem; border-radius:10px; background:#F8FAFC; border-left:3px solid #F59E0B;'>"
    "<div style='font-weight:800; color:#F59E0B; font-size:0.78rem; text-transform:uppercase;'>Phase 4</div>"
    "<div style='font-weight:700; color:#0F172A; font-size:0.92rem; margin:0.2rem 0;'>Explainability Layer</div>"
    "<div style='font-size:0.8rem; color:#64748B;'>Tree-SHAP attributions and Partial Dependence Plots (PDP) provide global and individual transparency.</div>"
    "</div>"
    "<div style='padding:0.85rem; border-radius:10px; background:#F8FAFC; border-left:3px solid #EF4444;'>"
    "<div style='font-weight:800; color:#EF4444; font-size:0.78rem; text-transform:uppercase;'>Phase 5</div>"
    "<div style='font-weight:700; color:#0F172A; font-size:0.92rem; margin:0.2rem 0;'>Triage &amp; Action</div>"
    "<div style='font-size:0.8rem; color:#64748B;'>Calibrated risk tier classification (0–29 Low, 30–59 Medium, 60–100 High) and CRM export.</div>"
    "</div>"
    "</div>"
    "</div>"
)
render_raw_html(pipeline_html)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Section 3: Technology Stack & Governance
# -----------------------------------------------------------------------------
display_section_header(
    "Enterprise Technology Stack",
    "Production software libraries, frameworks, and deployment environment.",
    accent_color="#10B981",
)

tech_col1, tech_col2, tech_col3 = st.columns(3, gap="medium")

with tech_col1:
    t1_html = (
        "<div class='card-surface card-gradient-blue' style='height:100%;'>"
        "<div class='card-header'><div class='card-icon card-icon-blue'>🐍</div><div><div class='card-title'>Core Runtime</div><h3 style='margin:0; font-size:1rem;'>Python 3.10+ / Streamlit</h3></div></div>"
        "<p style='font-size:0.85rem; color:#475569; line-height:1.6; margin-top:0.5rem;'>"
        "High-performance reactive frontend framework with custom CSS tokens, session caching, and responsive multipage navigation."
        "</p>"
        "</div>"
    )
    render_raw_html(t1_html)

with tech_col2:
    t2_html = (
        "<div class='card-surface card-gradient-purple' style='height:100%;'>"
        "<div class='card-header'><div class='card-icon card-icon-purple'>🤖</div><div><div class='card-title'>Machine Learning</div><h3 style='margin:0; font-size:1rem;'>Scikit-learn &amp; SHAP</h3></div></div>"
        "<p style='font-size:0.85rem; color:#475569; line-height:1.6; margin-top:0.5rem;'>"
        "GradientBoostingClassifier, StandardScaler, LabelEncoder, and TreeExplainer for mathematically rigorous attribution."
        "</p>"
        "</div>"
    )
    render_raw_html(t2_html)

with tech_col3:
    t3_html = (
        "<div class='card-surface card-gradient-green' style='height:100%;'>"
        "<div class='card-header'><div class='card-icon card-icon-green'>📊</div><div><div class='card-title'>Visual Analytics</div><h3 style='margin:0; font-size:1rem;'>Plotly &amp; Pandas</h3></div></div>"
        "<p style='font-size:0.85rem; color:#475569; line-height:1.6; margin-top:0.5rem;'>"
        "Interactive SVG/WebGL charts, custom dashboard color palette, and vector heatmaps with minimal overhead."
        "</p>"
        "</div>"
    )
    render_raw_html(t3_html)
