# =============================================================================
# SHAP DEPENDENCE PLOT COMPONENT - ENTERPRISE XAI EDITION
# =============================================================================

import matplotlib.pyplot as plt
import shap
import streamlit as st


def display_shap_dependence_chart(shap_values, X_test):
    """
    Render interactive SHAP Dependence plot with feature interaction dropdown and dynamic insight cards.
    """
    col_sel, col_info = st.columns([1.5, 2.5], gap="medium")
    with col_sel:
        st.markdown("<div style='margin-bottom:0.3rem; font-size:0.86rem; font-weight:700; color:#0F172A;'>Select Model Attribute for Non-Linear Analysis:</div>", unsafe_allow_html=True)
        selected_feature = st.selectbox(
            "Audited Feature",
            X_test.columns,
            index=0,
            label_visibility="collapsed",
            key="dependence_feature",
        )

    with col_info:
        st.markdown(
            """
            <div style="background:#F0F9FF; border:1px solid #BAE6FD; border-radius:10px; padding:0.6rem 0.95rem; font-size:0.82rem; color:#0369A1; line-height:1.45;">
                💡 <b>Dependence Analysis</b>: Plots the exact SHAP attribution value of the chosen feature across all test customers, automatically colored by the strongest interacting secondary feature.
            </div>
            """,
            unsafe_allow_html=True,
        )

    plt.close("all")
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=130)

    shap_val_array = shap_values.values if hasattr(shap_values, "values") else shap_values

    # Pass ax=ax to guarantee shap renders directly onto the created figure
    shap.dependence_plot(
        ind=selected_feature,
        shap_values=shap_val_array,
        features=X_test,
        interaction_index="auto",
        ax=ax,
        show=False,
    )
    plt.title(f"SHAP Non-Linear Dependence & Interaction Analysis · {selected_feature}", fontsize=11, fontweight="bold", pad=12, color="#0F172A")
    plt.tight_layout()

    st.pyplot(
        fig,
        clear_figure=True,
        use_container_width=True,
    )
    plt.close(fig)

    st.markdown(
        f"""
        <div style="margin-top:0.85rem; padding:0.9rem 1.15rem; background:#F0FDF4; border:1.5px solid #BBF7D0; border-radius:12px;">
            <div style="display:flex; align-items:center; gap:0.4rem; margin-bottom:0.25rem;">
                <span style="font-size:1.05rem;">📊</span>
                <span style="font-weight:700; color:#166534; font-size:0.9rem;">Non-Linear Threshold Insight: <u>{selected_feature}</u></span>
            </div>
            <div style="font-size:0.82rem; color:#475569; line-height:1.55;">
                • Points above <b>y = 0</b> increase the predicted likelihood of customer attrition.<br>
                • Points below <b>y = 0</b> exert a protective, churn-mitigating influence.<br>
                • Vertical dispersion across the same X value highlights non-linear interaction with secondary demographic and product features.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )