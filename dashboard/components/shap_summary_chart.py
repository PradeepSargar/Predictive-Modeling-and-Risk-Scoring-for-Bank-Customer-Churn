# =============================================================================
# SHAP SUMMARY BEESWARM PLOT COMPONENT - ENTERPRISE XAI EDITION
# =============================================================================

import streamlit as st
import shap
import matplotlib.pyplot as plt


def display_shap_summary_chart(shap_values, X_test):
    """
    Render high-DPI SHAP Summary beeswarm plot with executive interpretation guide.
    """
    plt.close("all")
    fig = plt.figure(figsize=(10, 5.8), dpi=130)

    # Use shap beeswarm summary
    shap.summary_plot(
        shap_values,
        X_test,
        show=False,
        plot_size=None,
    )
    plt.title("SHAP Feature Impact Distribution on Customer Churn (2,000 Test Accounts)", fontsize=11, fontweight="bold", pad=12, color="#0F172A")
    plt.tight_layout()

    st.pyplot(
        fig,
        clear_figure=True,
        use_container_width=True,
    )
    plt.close(fig)

    # Executive Interpretation & Key Insights Box
    st.markdown(
        """
        <div style="margin-top:0.85rem; padding:1rem 1.25rem; background:linear-gradient(135deg, #FAF5FF 0%, #FFFFFF 100%); border:1.5px solid #DDD6FE; border-radius:14px; box-shadow:0 4px 18px -2px rgba(168,85,247,0.06);">
            <div style="display:flex; align-items:center; gap:0.5rem; margin-bottom:0.45rem;">
                <div style="width:28px; height:28px; border-radius:6px; background:linear-gradient(135deg, #A855F7 0%, #7E22CE 100%); color:#FFFFFF; display:flex; align-items:center; justify-content:center; font-size:0.85rem; font-weight:700;">📌</div>
                <div style="font-weight:800; color:#5B21B6; font-size:0.92rem;">Executive Guide: Reading the SHAP Beeswarm Distribution</div>
            </div>
            <div style="display:grid; grid-template-columns: repeat(3, 1fr); gap:0.75rem; margin-top:0.6rem;">
                <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:10px; padding:0.65rem 0.85rem;">
                    <div style="font-weight:700; color:#0F172A; font-size:0.82rem; margin-bottom:2px;">📍 Y-Axis Ranking</div>
                    <div style="font-size:0.78rem; color:#64748B; line-height:1.45;">Features are arranged vertically by total global attribution. The topmost features have the strongest predictive sway.</div>
                </div>
                <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:10px; padding:0.65rem 0.85rem;">
                    <div style="font-weight:700; color:#0F172A; font-size:0.82rem; margin-bottom:2px;">↔️ Horizontal Impact</div>
                    <div style="font-size:0.78rem; color:#64748B; line-height:1.45;">Points to the <b>right (+SHAP)</b> escalate churn risk; points to the <b>left (-SHAP)</b> solidify customer retention.</div>
                </div>
                <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:10px; padding:0.65rem 0.85rem;">
                    <div style="font-weight:700; color:#0F172A; font-size:0.82rem; margin-bottom:2px;">🎨 Dot Color Coding</div>
                    <div style="font-size:0.78rem; color:#64748B; line-height:1.45;"><span style="color:#EF4444; font-weight:700;">Red dots</span> denote high feature values; <span style="color:#0284C7; font-weight:700;">Blue dots</span> denote low or baseline feature values.</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )