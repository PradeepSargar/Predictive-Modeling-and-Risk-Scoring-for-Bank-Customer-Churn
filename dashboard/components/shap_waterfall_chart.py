# =============================================================================
# SHAP WATERFALL PLOT COMPONENT - ENTERPRISE XAI EDITION
# =============================================================================

import matplotlib.pyplot as plt
import shap
import streamlit as st


def display_shap_waterfall_chart(shap_values, X_test):
    """
    Render individual prediction explanation waterfall plot with front-line RM talk track.
    """
    col_sel, col_desc = st.columns([1.5, 2.5], gap="medium")
    with col_sel:
        st.markdown("<div style='margin-bottom:0.25rem; font-size:0.84rem; font-weight:700; color:#0F172A;'>Select Test Account for Attribution Breakdown:</div>", unsafe_allow_html=True)
        customer_index = st.selectbox(
            "Account Selector",
            range(min(len(X_test), 500)),
            format_func=lambda x: f"Account Test Record #{x+1}",
            label_visibility="collapsed",
            key="waterfall_customer",
        )

    with col_desc:
        st.markdown(
            """
            <div style="background:#FFFBEB; border:1px solid #FDE68A; border-radius:10px; padding:0.5rem 0.85rem; font-size:0.8rem; color:#92400E; line-height:1.45;">
                🔍 <b>Local XAI Waterfall</b>: Deconstructs the exact step-by-step mathematical bridge from the cohort expected value <b>E[f(x)]</b> to this individual customer's specific output score <b>f(x)</b>.
            </div>
            """,
            unsafe_allow_html=True,
        )

    plt.close("all")
    fig = plt.figure(figsize=(10, 5.8), dpi=130)

    shap.plots.waterfall(
        shap_values[customer_index],
        show=False,
    )
    plt.title(f"Individual Customer SHAP Waterfall Attribution · Test Record #{customer_index + 1}", fontsize=11, fontweight="bold", pad=12, color="#0F172A")
    plt.tight_layout()

    st.pyplot(
        fig,
        clear_figure=True,
        use_container_width=True,
    )
    plt.close(fig)

    # Front-Line Relationship Manager (RM) Guidance Card
    st.markdown(
        """
        <div style="margin-top:0.85rem; padding:1rem 1.25rem; background:linear-gradient(135deg, #FEF2F2 0%, #FFFFFF 100%); border:1.5px solid #FECACA; border-radius:14px; box-shadow:0 4px 18px -2px rgba(239,68,68,0.06);">
            <div style="display:flex; align-items:center; gap:0.5rem; margin-bottom:0.35rem;">
                <div style="width:28px; height:28px; border-radius:6px; background:linear-gradient(135deg, #EF4444 0%, #DC2626 100%); color:#FFFFFF; display:flex; align-items:center; justify-content:center; font-size:0.85rem; font-weight:700;">🌊</div>
                <div style="font-weight:800; color:#991B1B; font-size:0.92rem;">Front-Line Relationship Manager (RM) Triage Breakdown</div>
            </div>
            <div style="display:grid; grid-template-columns: repeat(2, 1fr); gap:0.75rem; margin-top:0.5rem;">
                <div style="background:#FFFFFF; border:1px solid #FEE2E2; border-radius:10px; padding:0.65rem 0.85rem;">
                    <div style="font-weight:700; color:#DC2626; font-size:0.82rem; margin-bottom:2px;">🔴 Risk Escalators (+SHAP)</div>
                    <div style="font-size:0.78rem; color:#475569; line-height:1.45;">Attributes highlighted in red increase this customer's predicted attrition likelihood above the bank baseline. Address these in outreach conversations.</div>
                </div>
                <div style="background:#FFFFFF; border:1px solid #DBEAFE; border-radius:10px; padding:0.65rem 0.85rem;">
                    <div style="font-weight:700; color:#0284C7; font-size:0.82rem; margin-bottom:2px;">🔵 Retention Anchors (-SHAP)</div>
                    <div style="font-size:0.78rem; color:#475569; line-height:1.45;">Attributes highlighted in blue decrease churn risk. Leverage these positive ties (e.g. multi-product tenure, credit score) during client check-ins.</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )