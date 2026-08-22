# =============================================================================
# EXECUTIVE RECOMMENDATIONS COMPONENT
# =============================================================================

"""
Displays strategic, data-driven business recommendations
for executive leadership based on portfolio KPIs.
"""

import streamlit as st


def display_executive_recommendations(summary=None):
    """
    Render executive retention priorities dynamically based on dataset summary.
    """
    if summary is None:
        summary = {
            "churn_rate": 20.37,
            "inactive_customers": 4849,
            "active_customers": 5151,
            "average_balance": 76485.89,
            "average_age": 38.92,
        }

    inactive_cnt = summary.get("inactive_customers", 4849)
    avg_bal = summary.get("average_balance", 76485.89)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            f"""
            <div class="card-surface card-gradient-green" style="height:100%;">
                <div class="card-header">
                    <div class="card-icon card-icon-green">🎯</div>
                    <div>
                        <div class="card-title">Priority 1: Customer Engagement</div>
                        <h3 style="margin:0; font-size:1.05rem; color:#0F172A;">Re-engage {inactive_cnt:,} Inactive Customers</h3>
                    </div>
                </div>
                <p style="margin:0.75rem 0 0.5rem 0; font-size:0.86rem; color:#334155; line-height:1.6;">
                    Inactive membership is the <b>primary behavioral driver</b> of customer attrition. Active members churn at less than half the rate of inactive members.
                </p>
                <ul class="list-clean" style="margin-top:0.5rem;">
                    <li><span class="list-check">✓</span>Launch automated digital re-engagement sequences for dormant accounts (>60 days no login).</li>
                    <li><span class="list-check">✓</span>Incentivize mobile app adoption and direct-deposit activation with cash-back bonuses.</li>
                    <li><span class="list-check">✓</span>Target 15% reduction in inactive base over next 2 quarters.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div class="card-surface card-gradient-blue" style="height:100%;">
                <div class="card-header">
                    <div class="card-icon card-icon-blue">💰</div>
                    <div>
                        <div class="card-title">Priority 2: High-AUM Retention</div>
                        <h3 style="margin:0; font-size:1.05rem; color:#0F172A;">Protect ${avg_bal:,.0f}+ Balance Cohorts</h3>
                    </div>
                </div>
                <p style="margin:0.75rem 0 0.5rem 0; font-size:0.86rem; color:#334155; line-height:1.6;">
                    High-balance customers in Germany and France show elevated attrition sensitivity when holding single products.
                </p>
                <ul class="list-clean" style="margin-top:0.5rem;">
                    <li><span class="list-check">✓</span>Cross-sell 2nd and 3rd wealth/credit products to create structural switching barriers.</li>
                    <li><span class="list-check">✓</span>Assign dedicated Relationship Managers to accounts exceeding $100,000 balance.</li>
                    <li><span class="list-check">✓</span>Deploy real-time churn risk alert webhooks into CRM for immediate RM intervention.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('<div style="height:0.5rem;"></div>', unsafe_allow_html=True)

    col3, col4 = st.columns(2)

    with col3:
        st.markdown(
            """
            <div class="card-surface card-gradient-amber" style="height:100%;">
                <div class="card-header">
                    <div class="card-icon card-icon-amber">🌍</div>
                    <div>
                        <div class="card-title">Priority 3: Geographic Optimization</div>
                        <h3 style="margin:0; font-size:1.05rem; color:#0F172A;">German Market Churn Intervention</h3>
                    </div>
                </div>
                <p style="margin:0.75rem 0 0.5rem 0; font-size:0.86rem; color:#334155; line-height:1.6;">
                    German customers exhibit churn rates (~32%) nearly double that of France (~16%) and Spain (~17%).
                </p>
                <ul class="list-clean" style="margin-top:0.5rem;">
                    <li><span class="list-check">✓</span>Conduct focused German customer satisfaction audit to identify localized friction points.</li>
                    <li><span class="list-check">✓</span>Review regional fee structures and digital banking features in German branches.</li>
                    <li><span class="list-check">✓</span>Offer tailored localized product bundles matching German consumer preferences.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col4:
        st.markdown(
            """
            <div class="card-surface card-gradient-purple" style="height:100%;">
                <div class="card-header">
                    <div class="card-icon card-icon-purple">🏆</div>
                    <div>
                        <div class="card-title">Priority 4: Model-Driven Workflow</div>
                        <h3 style="margin:0; font-size:1.05rem; color:#0F172A;">Production ML Scoring Integration</h3>
                    </div>
                </div>
                <p style="margin:0.75rem 0 0.5rem 0; font-size:0.86rem; color:#334155; line-height:1.6;">
                    Leverage the Gradient Boosting champion model (86.31% ± 1.11% CV accuracy, 86.48% ± 1.10% ROC-AUC) for proactive retention.
                </p>
                <ul class="list-clean" style="margin-top:0.5rem;">
                    <li><span class="list-check">✓</span>Embed daily batch risk scoring into morning branch dispatch reports.</li>
                    <li><span class="list-check">✓</span>Use SHAP explainability waterfall plots to equip branch staff with specific retention talk tracks.</li>
                    <li><span class="list-check">✓</span>Run monthly A/B tests in the What-If Simulator before launching marketing campaigns.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )