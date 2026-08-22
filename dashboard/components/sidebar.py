import streamlit as st
import os

_BRAND_NAME = "Bank Churn Intelligence"
_BRAND_TAGLINE = "Predictive Risk & Retention Platform"
_DEVELOPER_NAME = "Pradeep Sargar"
_UNIVERSITY_NAME = "University of Mumbai"
_DEGREE_NAME = "Computer Engineering"


def _safe_page_link(page_path: str, label: str, icon: str):
    """Safely render page links resolving paths relative to root or pages/."""
    try:
        st.page_link(page_path, label=label, icon=icon)
    except Exception:
        try:
            alt_path = page_path if not page_path.startswith("pages/") else page_path[len("pages/"):]
            st.page_link(alt_path, label=label, icon=icon)
        except Exception:
            pass


def display_sidebar():
    with st.sidebar:
        st.markdown(
            f"""
            <div class="sidebar-brand">
                <div class="sidebar-logo">
                    <div class="sidebar-logo-mark">🏦</div>
                    <div>
                        <div class="sidebar-brand-name">{_BRAND_NAME}</div>
                        <div class="sidebar-brand-tagline">{_BRAND_TAGLINE}</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # -------------------------------------------------------------
        # Navigation Section: OVERVIEW
        # -------------------------------------------------------------
        st.markdown(
            """
            <div class="sidebar-section">
                <div class="sidebar-section-title">OVERVIEW</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        _safe_page_link("pages/01_Executive_Overview.py", label="01  Executive Overview", icon="👔")

        # -------------------------------------------------------------
        # Navigation Section: ANALYTICS
        # -------------------------------------------------------------
        st.markdown(
            """
            <div class="sidebar-section">
                <div class="sidebar-section-title">ANALYTICS</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        _safe_page_link("pages/02_Customer_Analytics.py", label="02  Customer Analytics", icon="📊")
        _safe_page_link("pages/03_Risk_Portfolio.py", label="03  Risk Portfolio", icon="🎯")

        # -------------------------------------------------------------
        # Navigation Section: MODELING
        # -------------------------------------------------------------
        st.markdown(
            """
            <div class="sidebar-section">
                <div class="sidebar-section-title">MODELING</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        _safe_page_link("pages/04_Model_Performance.py", label="04  Model Performance", icon="🏆")
        _safe_page_link("pages/05_Model_Explainability.py", label="05  Model Explainability", icon="🧠")

        # -------------------------------------------------------------
        # Navigation Section: RISK INTELLIGENCE
        # -------------------------------------------------------------
        st.markdown(
            """
            <div class="sidebar-section">
                <div class="sidebar-section-title">RISK INTELLIGENCE</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        _safe_page_link("pages/06_Customer_Risk_Scoring.py", label="06  Customer Risk Scoring", icon="🔮")
        _safe_page_link("pages/07_Scenario_Simulator.py", label="07  Scenario Simulator", icon="🎚️")

        # -------------------------------------------------------------
        # Navigation Section: PLATFORM
        # -------------------------------------------------------------
        st.markdown(
            """
            <div class="sidebar-section">
                <div class="sidebar-section-title">PLATFORM</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        _safe_page_link("pages/08_Platform_Overview.py", label="08  Platform Overview", icon="ℹ️")

        # -------------------------------------------------------------
        # System Status & Model Performance Metrics
        # -------------------------------------------------------------
        st.markdown(
            """
            <div class="sidebar-section" style="margin-top:0.75rem;">
                <div class="sidebar-section-title">SYSTEM STATUS</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.markdown(
                """
                <div class="sidebar-metric-card">
                    <div class="sidebar-metric-label">Model Engine</div>
                    <div class="sidebar-metric-value" style="color:#10B981 !important;">Ready</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with col_s2:
            st.markdown(
                """
                <div class="sidebar-metric-card">
                    <div class="sidebar-metric-label">Risk Scoring</div>
                    <div class="sidebar-metric-value" style="color:#10B981 !important;">Live</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown(
            """
            <div class="sidebar-metric-card">
                <div class="sidebar-metric-label">🎯 Champion Accuracy</div>
                <div class="sidebar-metric-value" style="font-size:1.02rem;">
                    86.31%
                    <span class="card-delta-positive" style="margin-left:0.3rem;">CV ROC: 86.48%</span>
                </div>
            </div>
            <div class="sidebar-metric-card">
                <div class="sidebar-metric-label">👥 Monitored Portfolio</div>
                <div class="sidebar-metric-value" style="font-size:1.02rem;">10,000 Accounts</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div class="sidebar-footer">
                <div style="margin-bottom:0.4rem;">
                    <span class="pill pill-blue" style="font-size:0.72rem;">v2.0.0 Enterprise</span>
                </div>
                <div class="footer-name">{_DEVELOPER_NAME}</div>
                <div class="footer-text">{_DEGREE_NAME} · {_UNIVERSITY_NAME}</div>
                <div style="margin-top:0.5rem;">
                    <div style="display:flex; align-items:center; gap:0.4rem; margin-bottom:0.2rem;">
                        <span style="width:7px; height:7px; border-radius:50%; background:#10B981; display:inline-block;"></span>
                        <span class="footer-text" style="color:#10B981 !important; font-weight:600;">System Operational</span>
                    </div>
                    <div class="footer-text" style="margin-top:0.25rem;">© 2026 {_BRAND_NAME}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
