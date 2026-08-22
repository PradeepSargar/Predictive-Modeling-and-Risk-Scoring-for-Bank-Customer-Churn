# =============================================================================
# MODEL PERFORMANCE CARDS COMPONENT
# =============================================================================

"""
Displays production Gradient Boosting model performance benchmarks (5-Fold CV).
"""

import streamlit as st


def display_model_performance_cards():
    """
    Render executive-styled model performance benchmark grid based on 5-Fold CV.
    """
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.markdown(
            """
            <div class="card-surface card-gradient-blue">
                <div class="card-header">
                    <div class="card-icon card-icon-blue">🎯</div>
                    <div class="card-title">CV Accuracy</div>
                </div>
                <div class="card-value" style="font-size:1.35rem;">86.31% ± 0.99%</div>
                <div class="card-subtitle">5-Fold CV Mean ± Std</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="card-surface card-gradient-green">
                <div class="card-header">
                    <div class="card-icon card-icon-green">🔍</div>
                    <div class="card-title">CV Precision</div>
                </div>
                <div class="card-value" style="font-size:1.35rem;">77.22% ± 3.17%</div>
                <div class="card-subtitle">Minimizes false alarms</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
            <div class="card-surface card-gradient-amber">
                <div class="card-header">
                    <div class="card-icon card-icon-amber">⚡</div>
                    <div class="card-title">CV Recall</div>
                </div>
                <div class="card-value" style="font-size:1.35rem;">46.44% ± 3.56%</div>
                <div class="card-subtitle">Churn capture sensitivity</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col4:
        st.markdown(
            """
            <div class="card-surface card-gradient-purple">
                <div class="card-header">
                    <div class="card-icon card-icon-purple">⚖️</div>
                    <div class="card-title">CV F1 Score</div>
                </div>
                <div class="card-value" style="font-size:1.35rem;">57.98% ± 3.65%</div>
                <div class="card-subtitle">Balanced harmonic metric</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col5:
        st.markdown(
            """
            <div class="card-surface card-gradient-purple">
                <div class="card-header">
                    <div class="card-icon card-icon-purple">📈</div>
                    <div class="card-title">CV ROC-AUC</div>
                </div>
                <div class="card-value" style="font-size:1.35rem;">86.48% ± 0.99%</div>
                <div class="card-subtitle">High discriminative power</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div style="margin-top:1.25rem; padding:1.1rem 1.35rem; background:#F8FAFC; border:1px solid #E2E8F0; border-radius:14px;">
            <div style="display:flex; align-items:center; gap:0.6rem; margin-bottom:0.35rem;">
                <span class="pill pill-green" style="font-size:0.75rem;">🏆 Champion Model</span>
                <span style="font-weight:700; color:#0F172A; font-size:0.95rem;">Gradient Boosting Classifier</span>
            </div>
            <div style="font-size:0.86rem; color:#475569; line-height:1.6;">
                The <b>Gradient Boosting Classifier</b> was selected for production over XGBoost, Random Forest, Logistic Regression, and Decision Tree.
                It provides the optimal balance of <b>86.31% ± 0.99% cross-validation accuracy</b> and <b>86.48% ± 0.99% ROC-AUC</b>, ensuring risk scores are calibrated, reliable, and auditable across all customer cohorts.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )