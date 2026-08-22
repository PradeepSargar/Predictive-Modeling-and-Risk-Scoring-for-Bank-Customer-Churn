# =============================================================================
# PARTIAL DEPENDENCE PLOT (PDP) COMPONENT - GRADIENT BOOSTING
# =============================================================================

"""
Renders Partial Dependence Plots (PDP) for the trained Gradient Boosting model.
PDP illustrates the marginal non-linear effect of one or more features on the predicted
churn probability across the customer test cohort (Pipeline Step 14).
"""

import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.inspection import partial_dependence


@st.cache_data(show_spinner=False)
def _compute_pdp_curves(_model, _X_test_pdp, selected_features_tuple, grid_res):
    curves = {}
    for feat in selected_features_tuple:
        res = partial_dependence(
            _model,
            _X_test_pdp,
            features=[feat],
            response_method="predict_proba",
            method="brute",
            kind="average",
            grid_resolution=grid_res,
        )
        avg = res["average"][0] if "average" in res else res[0][0]
        vals = res["grid_values"][0] if "grid_values" in res else res["values"][0]
        curves[feat] = (vals, avg)
    return curves


def display_partial_dependence_chart(gradient_boosting_model, X_test, feature_importance_df=None):
    """
    Render interactive Partial Dependence Plots for top influential features.
    """
    if gradient_boosting_model is None or X_test is None:
        st.warning("Model or test dataset not available for Partial Dependence analysis.")
        return

    # Ensure numeric float dtype to satisfy scikit-learn continuous PDP requirement
    X_test_pdp = X_test.copy()
    num_cols = X_test_pdp.select_dtypes(include=["number"]).columns
    X_test_pdp[num_cols] = X_test_pdp[num_cols].astype(float)

    # Determine default top features from feature importance if available
    if feature_importance_df is not None and "Feature" in feature_importance_df.columns:
        default_top = [f for f in feature_importance_df["Feature"].tolist() if f in X_test_pdp.columns][:5]
    else:
        default_top = ["Age", "NumOfProducts", "Balance", "IsActiveMember", "CreditScore"]
        default_top = [f for f in default_top if f in X_test_pdp.columns]

    st.markdown(
        """
        <div style="background:#F0F9FF; border:1px solid #BAE6FD; border-radius:10px; padding:0.75rem 1rem; margin-bottom:1rem; font-size:0.84rem; color:#0369A1; line-height:1.5;">
            📈 <b>Partial Dependence Plot (PDP) Analysis (Pipeline Step 14)</b>: Demonstrates the marginal relationship between customer features and predicted churn probability. 
            Unlike SHAP (which decomposes individual customer instances), PDP computes the average expected change in predicted churn probability when systematically varying a feature across the entire cohort.
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_ctrl1, col_ctrl2 = st.columns([2, 1], gap="medium")
    with col_ctrl1:
        selected_features = st.multiselect(
            "Select Features for PDP Analysis (Top 1–5 recommended):",
            options=X_test_pdp.columns.tolist(),
            default=default_top[:4] if len(default_top) >= 4 else default_top,
            key="pdp_feature_multiselect",
        )
    with col_ctrl2:
        grid_res = st.slider("Grid Resolution", min_value=20, max_value=80, value=40, step=10, key="pdp_grid_res")

    if not selected_features:
        st.info("Please select at least one feature to display Partial Dependence Plots.")
        return

    try:
        with st.spinner("Generating Partial Dependence curves..."):
            curves = _compute_pdp_curves(
                gradient_boosting_model,
                X_test_pdp,
                tuple(selected_features),
                grid_res
            )

            n_features = len(selected_features)
            n_cols = min(2, n_features)
            n_rows = (n_features + n_cols - 1) // n_cols

            plt.close("all")
            fig, ax = plt.subplots(
                nrows=n_rows,
                ncols=n_cols,
                figsize=(6.5 * n_cols, 3.8 * n_rows),
                dpi=120,
                squeeze=False,
            )

            ax_flat = ax.flatten()

            for idx, feat in enumerate(selected_features):
                vals, avg = curves[feat]
                a = ax_flat[idx]
                a.plot(vals, avg, color="#0284C7", linewidth=2.5)
                a.fill_between(vals, avg, min(avg), alpha=0.08, color="#0EA5E9")
                a.set_ylabel("Predicted Churn Probability", fontsize=9, color="#475569")
                a.set_xlabel(feat, fontsize=9, fontweight="600", color="#0F172A")
                a.grid(True, linestyle="--", alpha=0.3, color="#94A3B8")
                a.tick_params(labelsize=8)
                a.set_title(f"PDP: {feat}", fontsize=10, fontweight="700", color="#0F172A", pad=8)

            # Hide any unused subplots
            for idx in range(n_features, len(ax_flat)):
                fig.delaxes(ax_flat[idx])

            fig.suptitle(
                "Partial Dependence Curves · Champion Gradient Boosting",
                fontsize=12,
                fontweight="bold",
                color="#0F172A",
                y=1.02,
            )
            plt.tight_layout()

            st.pyplot(fig, clear_figure=True, use_container_width=True)
            plt.close(fig)

    except Exception as exc:
        st.error(f"Error computing Partial Dependence: {exc}")

    st.markdown(
        """
        <div style="margin-top:0.85rem; padding:0.9rem 1.15rem; background:#F8FAFC; border:1px solid #E2E8F0; border-radius:12px;">
            <div style="font-weight:700; color:#0F172A; font-size:0.88rem; margin-bottom:0.3rem;">💡 Business Interpretation of PDP Trends</div>
            <div style="font-size:0.82rem; color:#475569; line-height:1.55;">
                • <b>Upward Slope</b>: As feature value rises (e.g. Age > 40), average predicted churn probability increases, highlighting demographic segments requiring proactive outreach.<br>
                • <b>Downward Slope / Inverted U-Shape</b>: As product holdings or engagement status increase, baseline risk shifts downward.<br>
                • <b>Threshold Plateaus</b>: Non-linear flattening reveals stability inflection points where marginal retention ROI is maximized.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )