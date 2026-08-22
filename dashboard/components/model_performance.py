# =============================================================================
# MODEL PERFORMANCE COMPONENT
# =============================================================================

"""
Displays the benchmark metrics of the deployed Gradient Boosting champion model.
"""

import streamlit as st


def display_model_performance():
    """
    Render styled champion model performance metric cards (5-Fold CV Means).
    """
    metrics = [
        {"label": "CV Accuracy", "value": "86.31% ± 0.99%", "sub": "5-Fold CV Mean ± Std", "variant": "blue", "icon": "🎯"},
        {"label": "CV ROC-AUC", "value": "86.48% ± 0.99%", "sub": "High discriminative power", "variant": "purple", "icon": "📈"},
        {"label": "CV Precision", "value": "77.22% ± 3.17%", "sub": "High-conviction touches", "variant": "green", "icon": "🔍"},
        {"label": "CV Recall", "value": "46.44% ± 3.56%", "sub": "Baseline churn capture", "variant": "amber", "icon": "⚡"},
        {"label": "CV F1 Score", "value": "57.98% ± 3.65%", "sub": "Harmonic balance", "variant": "purple", "icon": "⚖️"},
        {"label": "Champion Model", "value": "Gradient Boosting", "sub": "Tuned ensemble", "variant": "green", "icon": "🏆"},
    ]

    cols = st.columns(6)
    for i, m in enumerate(metrics):
        with cols[i]:
            st.markdown(
                f"""
                <div class="card-surface card-gradient-{m['variant']}" style="padding:0.9rem 1rem;">
                    <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:0.25rem;">
                        <span class="card-title" style="font-size:0.75rem;">{m['label']}</span>
                        <span style="font-size:0.95rem;">{m['icon']}</span>
                    </div>
                    <div class="card-value" style="font-size:1.15rem; margin-bottom:0.15rem;">{m['value']}</div>
                    <div style="font-size:0.72rem; color:#64748B;">{m['sub']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )