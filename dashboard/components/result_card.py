import streamlit as st
from utils.constants import LOW_RISK_THRESHOLD, MEDIUM_RISK_THRESHOLD


def display_prediction_result(prediction_label, probability, risk_level):
    risk_score = round(probability * 100, 1)

    if probability >= MEDIUM_RISK_THRESHOLD:
        risk_class = "risk-high"
        risk_icon = "🔴"
        risk_label = "High Churn Risk"
        risk_title = "Elevated Likelihood of Attrition"
        risk_desc = (
            "The customer exhibits an elevated statistical likelihood of attrition. Proactive, high-priority retention "
            "intervention is strongly recommended to safeguard this account relationship."
        )
        confidence = "High"
        banner_bg = "linear-gradient(135deg, #DC2626 0%, #B91C1C 100%)"

    elif probability >= LOW_RISK_THRESHOLD:
        risk_class = "risk-medium"
        risk_icon = "🟡"
        risk_label = "Medium Churn Risk"
        risk_title = "Moderate Attrition Risk"
        risk_desc = (
            "The customer exhibits a moderate churn signal. Proactive engagement, tailored bundle offers, "
            "and close monitoring of product utilization are recommended over the upcoming cycle."
        )
        confidence = "Medium"
        banner_bg = "linear-gradient(135deg, #D97706 0%, #B45309 100%)"

    else:
        risk_class = "risk-low"
        risk_icon = "🟢"
        risk_label = "Low Churn Risk"
        risk_title = "Stable Retention Profile"
        risk_desc = (
            "The customer demonstrates strong relationship stability. Focus on customer lifetime value growth: cross-sell, "
            "deepen deposit holdings, and introduce premium banking features."
        )
        confidence = "Low"
        banner_bg = "linear-gradient(135deg, #059669 0%, #047857 100%)"

    st.markdown(
        f"""
        <div style="background:{banner_bg}; color:#FFFFFF; border-radius:14px; padding:1.15rem 1.4rem; margin-bottom:1rem; box-shadow:0 2px 8px rgba(0,0,0,0.08);">
            <div style="display:flex; align-items:flex-start; justify-content:space-between; gap:1rem; flex-wrap:wrap;">
                <div style="display:flex; align-items:flex-start; gap:0.85rem; flex:1; min-width:260px;">
                    <div style="font-size:1.6rem; line-height:1; flex-shrink:0; margin-top:2px;">{risk_icon}</div>
                    <div>
                        <div style="font-size:0.75rem; font-weight:700; letter-spacing:0.06em; text-transform:uppercase; color:rgba(255,255,255,0.9); margin-bottom:0.15rem;">Risk Classification</div>
                        <div style="font-size:1.25rem; font-weight:800; color:#FFFFFF; line-height:1.2; margin-bottom:0.25rem;">{risk_title}</div>
                        <div style="font-size:0.86rem; color:#F8FAFC; line-height:1.45; font-weight:500;">{risk_desc}</div>
                    </div>
                </div>
                <div style="flex-shrink:0; text-align:right; min-width:120px;">
                    <div style="font-size:0.74rem; font-weight:700; letter-spacing:0.06em; text-transform:uppercase; color:rgba(255,255,255,0.9); margin-bottom:0.15rem;">
                        Risk Score (0–100)
                    </div>
                    <div style="font-size:2.2rem; font-weight:800; color:#FFFFFF; line-height:1; margin-bottom:0.2rem;">
                        {risk_score:.0f}
                    </div>
                    <div style="font-size:0.78rem; font-weight:700; color:#FFFFFF;">
                        {risk_label} ({probability:.1%})
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_pred, col_prob, col_risk = st.columns(3)

    with col_pred:
        prediction_variant = "red" if probability >= 0.5 else "green"
        prediction_icon = "⚠️" if probability >= 0.5 else "✅"
        st.markdown(
            f"""
            <div class="card-surface card-gradient-{prediction_variant}">
                <div class="card-header">
                    <div class="card-icon card-icon-{prediction_variant}">{prediction_icon}</div>
                    <div class="card-title">Prediction Outcome</div>
                </div>
                <div class="card-value" style="font-size:1.45rem; line-height:1.25;">
                    {prediction_label}
                </div>
                <div class="card-subtitle">Calibrated classification by Gradient Boosting champion model.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_prob:
        if probability >= MEDIUM_RISK_THRESHOLD:
            bar_color = "#DC2626"
            val_color = "#DC2626"
            prob_icon = "📉"
            prob_variant = "red"
        elif probability >= LOW_RISK_THRESHOLD:
            bar_color = "#D97706"
            val_color = "#D97706"
            prob_icon = "📊"
            prob_variant = "amber"
        else:
            bar_color = "#059669"
            val_color = "#059669"
            prob_icon = "📈"
            prob_variant = "green"

        pct = probability * 100

        st.markdown(
            f"""
            <div class="card-surface card-gradient-{prob_variant}">
                <div class="card-header">
                    <div class="card-icon card-icon-{prob_variant}">{prob_icon}</div>
                    <div class="card-title">Churn Probability &amp; Score</div>
                </div>
                <div style="margin:0.25rem 0;">
                    <span class="card-value" style="color:{val_color} !important; font-size:1.85rem;">{probability:.1%}</span>
                    <span style="font-size:0.78rem; color:#475569; font-weight:600; margin-left:0.35rem;">
                        (Score: {risk_score:.1f} / 100)
                    </span>
                </div>
                <div style="height:8px; background:#E2E8F0; border-radius:999px; overflow:hidden; margin:0.45rem 0 0.3rem 0;">
                    <div style="width:{pct:.1f}%; height:100%; background:{bar_color}; border-radius:999px;"></div>
                </div>
                <div style="display:flex; justify-content:space-between; font-size:0.72rem; color:#475569; font-weight:600;">
                    <span>0 (Low &lt;30)</span>
                    <span>30 (Medium)</span>
                    <span>60 (High)</span>
                    <span>100</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_risk:
        if probability >= MEDIUM_RISK_THRESHOLD:
            risk_icon2 = "🔴"
            risk_variant = "red"
            risk_value = "High Risk (60–100)"
            conf_variant = "red"
            conf_value = "High Priority"
        elif probability >= LOW_RISK_THRESHOLD:
            risk_icon2 = "🟡"
            risk_variant = "amber"
            risk_value = "Medium Risk (30–59)"
            conf_variant = "amber"
            conf_value = "Moderate Priority"
        else:
            risk_icon2 = "🟢"
            risk_variant = "green"
            risk_value = "Low Risk (0–29)"
            conf_variant = "green"
            conf_value = "Standard Growth"

        st.markdown(
            f"""
            <div class="card-surface card-gradient-{risk_variant}">
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.8rem; height:100%; align-content:center;">
                    <div>
                        <div class="card-title" style="margin-bottom:0.25rem;">Calibrated Risk Tier</div>
                        <div style="display:flex; align-items:center; gap:0.45rem;">
                            <span style="font-size:1.15rem;">{risk_icon2}</span>
                            <span style="font-size:1.15rem; font-weight:800; color:#0F172A;">
                                {risk_value}
                            </span>
                        </div>
                    </div>
                    <div>
                        <div class="card-title" style="margin-bottom:0.25rem;">Retention Urgency</div>
                        <div style="display:flex; align-items:center; gap:0.45rem;">
                            <span class="pill pill-{conf_variant}">
                                {conf_value}
                            </span>
                        </div>
                        <div style="font-size:0.78rem; color:#475569; margin-top:0.35rem; font-weight:600;">
                            Signal Level: <b>{confidence}</b>
                        </div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
