# =============================================================================
# EXECUTIVE BRAND HEADER COMPONENT
# =============================================================================

"""
Compact, high-density glassmorphic brand header for all dashboard pages.
Follows the Sky Blue / Dark Navy Enterprise visual design language.
"""

import streamlit as st


def display_brand_header(
    title="Bank Customer Churn Prediction",
    subtitle="Predictive Analytics & Risk Intelligence Platform",
    badges=None,
    icon="🏦",
):
    """
    Render a compact, high-impact executive brand header with inline status badges.
    """
    if badges is None:
        badges = [
            ("🏆", "Champion: Gradient Boosting"),
            ("🎯", "86.31% CV Accuracy"),
            ("📈", "86.48% CV ROC-AUC"),
            ("⚡", "Live Scoring Engine"),
        ]

    badges_html = "".join([
        f'<span class="brand-badge"><span>{b_icon}</span><span>{text}</span></span>'
        for b_icon, text in badges
    ])

    st.markdown(
        f"""
        <div class="brand-header">
            <div class="brand-header-inner">
                <div style="display:flex; align-items:center; justify-content:space-between; gap:1.25rem; flex-wrap:wrap;">
                    <div style="display:flex; align-items:center; gap:0.85rem; flex:1; min-width:280px;">
                        <div class="brand-header-icon">{icon}</div>
                        <div>
                            <h1 class="brand-title">{title}</h1>
                            <p class="brand-subtitle">{subtitle}</p>
                        </div>
                    </div>
                    <div class="brand-badges">
                        {badges_html}
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def display_page_title(title, description=None):
    desc_html = f'<p class="page-description" style="font-size:0.86rem; color:#64748B; margin-top:0.2rem;">{description}</p>' if description else ""
    st.markdown(
        f"""
        <div class="page-title-wrapper" style="margin-bottom:1.15rem;">
            <h2 class="page-title" style="font-size:1.4rem; font-weight:800; color:#0F172A; margin:0;">{title}</h2>
            {desc_html}
        </div>
        """,
        unsafe_allow_html=True,
    )
