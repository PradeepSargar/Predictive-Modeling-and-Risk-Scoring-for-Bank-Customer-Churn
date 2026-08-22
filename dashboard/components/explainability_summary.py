# =============================================================================
# EXPLAINABILITY GOVERNANCE & METHODOLOGY COMPONENT - ENTERPRISE XAI EDITION
# =============================================================================

import streamlit as st


def display_explainability_summary():
    """
    Render comprehensive enterprise XAI methodology and regulatory governance framework.
    """
    # Top 4-card methodology architecture
    st.markdown(
        """
        <div style="display:grid; grid-template-columns: repeat(4, 1fr); gap:0.75rem; margin-bottom:1.15rem;">
            <div style="background:#FFFFFF; border:1px solid #BAE6FD; border-radius:12px; padding:0.9rem 1rem; box-shadow:0 2px 6px rgba(14,165,233,0.06);">
                <div style="display:flex; align-items:center; gap:0.5rem; margin-bottom:0.35rem;">
                    <div style="width:30px; height:30px; border-radius:8px; background:#E0F2FE; color:#0284C7; display:flex; align-items:center; justify-content:center; font-size:1rem;">🧠</div>
                    <div style="font-weight:800; font-size:0.88rem; color:#0F172A;">Game Theory</div>
                </div>
                <div style="font-size:0.78rem; color:#64748B; line-height:1.45;">
                    Built on <b>Lloyd Shapley's Nobel Prize-winning framework</b> (1953), ensuring mathematically unique and fair payoff allocations across all features.
                </div>
            </div>
            <div style="background:#FFFFFF; border:1px solid #DDD6FE; border-radius:12px; padding:0.9rem 1rem; box-shadow:0 2px 6px rgba(168,85,247,0.06);">
                <div style="display:flex; align-items:center; gap:0.5rem; margin-bottom:0.35rem;">
                    <div style="width:30px; height:30px; border-radius:8px; background:#F3E8FF; color:#7E22CE; display:flex; align-items:center; justify-content:center; font-size:1rem;">🌳</div>
                    <div style="font-weight:800; font-size:0.88rem; color:#0F172A;">TreeExplainer</div>
                </div>
                <div style="font-size:0.78rem; color:#64748B; line-height:1.45;">
                    Utilizes exact polynomial time tree-traversal <b>O(TLD²)</b> rather than sampling approximations, guaranteeing 100% deterministic attribution values.
                </div>
            </div>
            <div style="background:#FFFFFF; border:1px solid #A7F3D0; border-radius:12px; padding:0.9rem 1rem; box-shadow:0 2px 6px rgba(16,185,129,0.06);">
                <div style="display:flex; align-items:center; gap:0.5rem; margin-bottom:0.35rem;">
                    <div style="width:30px; height:30px; border-radius:8px; background:#D1FAE5; color:#065F46; display:flex; align-items:center; justify-content:center; font-size:1rem;">⚖️</div>
                    <div style="font-weight:800; font-size:0.88rem; color:#0F172A;">SR 11-7 / GDPR</div>
                </div>
                <div style="font-size:0.78rem; color:#64748B; line-height:1.45;">
                    Fully complies with <b>Federal Reserve SR 11-7</b> model risk management guidance and <b>GDPR Article 22</b> requirements for automated decision transparency.
                </div>
            </div>
            <div style="background:#FFFFFF; border:1px solid #FDE68A; border-radius:12px; padding:0.9rem 1rem; box-shadow:0 2px 6px rgba(245,158,11,0.06);">
                <div style="display:flex; align-items:center; gap:0.5rem; margin-bottom:0.35rem;">
                    <div style="width:30px; height:30px; border-radius:8px; background:#FEF3C7; color:#92400E; display:flex; align-items:center; justify-content:center; font-size:1rem;">🛡️</div>
                    <div style="font-weight:800; font-size:0.88rem; color:#0F172A;">Audit Trail</div>
                </div>
                <div style="font-size:0.78rem; color:#64748B; line-height:1.45;">
                    Every scored account records an immutable record of baseline risk, top 3 positive contributors, and top 3 negative contributors for internal audit review.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Detailed Governance Matrix
    st.markdown(
        """
        <div style="background:linear-gradient(135deg, #F8FAFC 0%, #FFFFFF 100%); border:1.5px solid #BAE6FD; border-radius:14px; padding:1.25rem 1.4rem; box-shadow:0 4px 18px -2px rgba(14,165,233,0.06);">
            <div style="font-weight:800; color:#0F172A; font-size:1rem; margin-bottom:0.6rem;">
                🏛️ Institutional XAI Governance &amp; Model Fairness Standards
            </div>
            <div style="font-size:0.86rem; color:#334155; line-height:1.65;">
                In enterprise banking, machine learning classifiers must never operate as opaque black boxes. 
                Our Explainability Architecture enforces three rigorous operational constraints:
            </div>
            <div style="display:grid; grid-template-columns: repeat(3, 1fr); gap:1rem; margin-top:0.85rem;">
                <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:10px; padding:0.85rem 1rem;">
                    <div style="font-weight:700; color:#0284C7; font-size:0.86rem; margin-bottom:0.25rem;">1. Additive Efficiency</div>
                    <div style="font-size:0.8rem; color:#64748B; line-height:1.5;">The sum of individual SHAP values across all 11 features precisely equals the difference between the customer score and the baseline expected value: <b>∑ φᵢ = f(x) - E[f(x)]</b>.</div>
                </div>
                <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:10px; padding:0.85rem 1rem;">
                    <div style="font-weight:700; color:#7E22CE; font-size:0.86rem; margin-bottom:0.25rem;">2. Bias &amp; Demographic Parity</div>
                    <div style="font-size:0.8rem; color:#64748B; line-height:1.5;">Continuous monitoring verifies that demographic flags (e.g. Gender) do not generate disproportionate attribution without empirical correlation to financial tenure.</div>
                </div>
                <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:10px; padding:0.85rem 1rem;">
                    <div style="font-weight:700; color:#059669; font-size:0.86rem; margin-bottom:0.25rem;">3. Model Risk Governance</div>
                    <div style="font-size:0.8rem; color:#64748B; line-height:1.5;">Model drift, feature attribution stability, and decision boundary calibration are re-evaluated quarterly against holdout test datasets.</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )