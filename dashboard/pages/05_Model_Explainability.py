# =============================================================================
# MODEL EXPLAINABILITY (XAI) SUITE - COMPACT ENTERPRISE TEMPLATE
# =============================================================================

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st

from components.theme import apply_global_theme
from components.sidebar import display_sidebar
from components.section_header import display_section_header

from services.explainability_service import ExplainabilityService
from services.model_loader import load_models

from components.explainability_summary import display_explainability_summary
from components.feature_importance_chart import display_feature_importance_chart
from components.shap_summary_chart import display_shap_summary_chart
from components.shap_dependence_chart import display_shap_dependence_chart
from components.shap_waterfall_chart import display_shap_waterfall_chart
from components.partial_dependence_chart import display_partial_dependence_chart
from utils.helpers import render_error_banner


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
    page_title="Model Explainability | Bank Churn Intelligence",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_global_theme()
display_sidebar()

# -----------------------------------------------------------------------------
# Compact Hero Header & Status Ribbon
# -----------------------------------------------------------------------------
compact_header_html = (
    "<div style='background:linear-gradient(135deg, #F0F9FF 0%, #FFFFFF 100%); border:1px solid #BAE6FD; border-radius:14px; padding:0.9rem 1.25rem; margin-bottom:0.75rem; box-shadow:0 4px 18px -2px rgba(14,165,233,0.06);'>"
    "<div style='display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.5rem;'>"
    "<div style='display:flex; align-items:center; gap:0.75rem;'>"
    "<div style='width:36px; height:36px; border-radius:10px; background:linear-gradient(135deg, #0EA5E9 0%, #0284C7 100%); color:#FFFFFF; display:flex; align-items:center; justify-content:center; font-size:1.15rem; font-weight:700;'>🧠</div>"
    "<div>"
    "<h1 style='margin:0; font-size:1.25rem; font-weight:800; color:#0F172A; line-height:1.2;'>Model Explainability (XAI) Suite</h1>"
    "<div style='font-size:0.8rem; color:#64748B; margin-top:2px;'>Auditable machine learning — global feature importance rankings, partial dependencies (PDP), and local SHAP attributions.</div>"
    "</div>"
    "</div>"
    "<div style='display:flex; align-items:center; gap:0.4rem; flex-wrap:wrap;'>"
    "<span class='pill pill-purple' style='font-size:0.72rem; padding:0.2rem 0.55rem;'>🧠 SHAP TreeExplainer</span>"
    "<span class='pill pill-blue' style='font-size:0.72rem; padding:0.2rem 0.55rem;'>📈 Global PDP &amp; Importance</span>"
    "<span class='pill pill-blue' style='font-size:0.72rem; padding:0.2rem 0.55rem;'>🌊 Waterfall Attribution</span>"
    "<span class='pill pill-green' style='font-size:0.72rem; padding:0.2rem 0.55rem;'>✅ Regulatory Compliant</span>"
    "</div>"
    "</div>"
    "</div>"
)
render_raw_html(compact_header_html)

# -----------------------------------------------------------------------------
# Compact 4-Metric Horizontal Stat Ribbon
# -----------------------------------------------------------------------------
stat_ribbon_html = (
    "<div style='display:grid; grid-template-columns: repeat(4, 1fr); gap:0.65rem; margin-bottom:0.85rem;'>"
    "<div style='background:#FFFFFF; border:1px solid #E2E8F0; border-radius:10px; padding:0.55rem 0.85rem; display:flex; align-items:center; gap:0.6rem;'>"
    "<div style='font-size:1.1rem;'>🧠</div>"
    "<div>"
    "<div style='font-size:0.68rem; color:#64748B; font-weight:600; text-transform:uppercase;'>XAI Engine</div>"
    "<div style='font-size:0.92rem; font-weight:800; color:#0F172A;'>Tree-SHAP &amp; PDP</div>"
    "</div>"
    "</div>"
    "<div style='background:#FFFFFF; border:1px solid #E2E8F0; border-radius:10px; padding:0.55rem 0.85rem; display:flex; align-items:center; gap:0.6rem;'>"
    "<div style='font-size:1.1rem;'>🧬</div>"
    "<div>"
    "<div style='font-size:0.68rem; color:#64748B; font-weight:600; text-transform:uppercase;'>Audited Features</div>"
    "<div style='font-size:0.92rem; font-weight:800; color:#0284C7;'>11 Features</div>"
    "</div>"
    "</div>"
    "<div style='background:#FFFFFF; border:1px solid #E2E8F0; border-radius:10px; padding:0.55rem 0.85rem; display:flex; align-items:center; gap:0.6rem;'>"
    "<div style='font-size:1.1rem;'>📊</div>"
    "<div>"
    "<div style='font-size:0.68rem; color:#64748B; font-weight:600; text-transform:uppercase;'>Explainer Samples</div>"
    "<div style='font-size:0.92rem; font-weight:800; color:#D97706;'>2,000 Test Set</div>"
    "</div>"
    "</div>"
    "<div style='background:#FFFFFF; border:1px solid #E2E8F0; border-radius:10px; padding:0.55rem 0.85rem; display:flex; align-items:center; gap:0.6rem;'>"
    "<div style='font-size:1.1rem;'>🎯</div>"
    "<div>"
    "<div style='font-size:0.68rem; color:#64748B; font-weight:600; text-transform:uppercase;'>Top Global Driver</div>"
    "<div style='font-size:0.92rem; font-weight:800; color:#DC2626;'>Age &amp; Products</div>"
    "</div>"
    "</div>"
    "</div>"
)
render_raw_html(stat_ribbon_html)

try:
    feature_importance_df = ExplainabilityService.load_feature_importance()
    shap_values = ExplainabilityService.load_shap_values()
    X_test = ExplainabilityService.load_x_test()
    gradient_boosting_model, _, _ = load_models()
    explainability_loaded = True
except Exception as error:
    explainability_loaded = False
    error_message = error

if not explainability_loaded:
    render_error_banner(
        title="Explainability Artifacts Missing",
        detail=str(error_message),
        suggestion="Verify that shap_values.pkl, feature_importance.pkl, and X_test.pkl exist in /models/.",
    )
    st.stop()

# -----------------------------------------------------------------------------
# Structured 6-Tab Explainability Suite
# -----------------------------------------------------------------------------
tab_feat, tab_summary, tab_pdp, tab_dep, tab_waterfall, tab_overview = st.tabs([
    "📈 Tab 1: Global Feature Importance",
    "🧠 Tab 2: SHAP Summary Beeswarm",
    "📊 Tab 3: Partial Dependence Plot (PDP)",
    "📉 Tab 4: SHAP Feature Dependence",
    "🌊 Tab 5: Local Waterfall Attribution",
    "📋 Tab 6: Governance & Methodology",
])

with tab_feat:
    display_feature_importance_chart(feature_importance_df)

with tab_summary:
    display_shap_summary_chart(shap_values, X_test)

with tab_pdp:
    display_partial_dependence_chart(gradient_boosting_model, X_test, feature_importance_df)

with tab_dep:
    display_shap_dependence_chart(shap_values, X_test)

with tab_waterfall:
    display_shap_waterfall_chart(shap_values, X_test)

with tab_overview:
    display_explainability_summary()

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

guidance_card_html = (
    "<div style='margin-top:0.25rem; padding:0.9rem 1.25rem; border-radius:12px; background:#FAF5FF; border:1px solid #DDD6FE;'>"
    "<div style='display:flex; align-items:flex-start; gap:0.75rem;'>"
    "<div style='width:32px; height:32px; border-radius:8px; background:linear-gradient(135deg, #A855F7 0%, #7E22CE 100%); color:#FFFFFF; display:flex; align-items:center; justify-content:center; font-size:0.95rem; flex-shrink:0;'>🧭</div>"
    "<div style='flex:1;'>"
    "<div style='font-weight:700; font-size:0.9rem; color:#0F172A; margin-bottom:0.15rem;'>How Banking Teams Utilize These Explanations</div>"
    "<div style='font-size:0.82rem; color:#475569; line-height:1.55;'>"
    "• <b>Global Views</b> (Feature Importance, SHAP Summary, Dependence) guide macro retention policies — such as targeting older inactive customers with bundle offers.<br>"
    "• <b>Local Views</b> (Waterfall Plot) equip front-line branch staff and Relationship Managers with specific talk tracks when speaking to individual high-risk clients."
    "</div>"
    "</div>"
    "</div>"
    "</div>"
)
render_raw_html(guidance_card_html)
