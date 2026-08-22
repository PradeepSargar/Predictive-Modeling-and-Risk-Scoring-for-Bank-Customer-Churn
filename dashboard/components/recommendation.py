import streamlit as st
from utils.constants import LOW_RISK_THRESHOLD, MEDIUM_RISK_THRESHOLD


def display_recommendation(probability):

    if probability >= MEDIUM_RISK_THRESHOLD:

        st.markdown(
            """
            <div style="background:#FEF2F2; border:1px solid #FECACA; border-radius:14px; padding:1rem 1.35rem; margin-bottom:1rem; display:flex; align-items:flex-start; gap:0.85rem; box-shadow:0 4px 18px -2px rgba(239,68,68,0.05);">
                <div style="width:40px; height:40px; border-radius:10px; background:linear-gradient(135deg, #EF4444 0%, #DC2626 100%); color:#FFFFFF; display:flex; align-items:center; justify-content:center; font-size:1.15rem; flex-shrink:0; box-shadow:0 3px 10px rgba(239,68,68,0.28);">🚨</div>
                <div style="flex:1;">
                    <div style="font-size:0.74rem; font-weight:700; letter-spacing:0.06em; text-transform:uppercase; color:#991B1B; margin-bottom:0.15rem;">Retention Priority</div>
                    <div style="font-size:1.1rem; font-weight:800; color:#7F1D1D; line-height:1.2;">Immediate Action Required · Priority 1 Account</div>
                    <div style="font-size:0.84rem; color:#991B1B; margin-top:0.2rem; line-height:1.45;">Escalate to relationship management. 24-hour response SLA applies.</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        actions_html = """
        <div class="action-card">
            <div class="action-card-header">
                <div class="action-card-icon" style="background:linear-gradient(135deg,#EF4444 0%,#DC2626 100%); color:#FFFFFF; box-shadow:0 2px 8px rgba(239,68,68,0.25);">📞</div>
                <div class="action-card-title">Direct Outreach within 24 Hours</div>
            </div>
            <div style="font-size:0.84rem; color:#334155; line-height:1.55; padding-left:3.2rem;">
                Schedule a personal call from the customer's assigned Relationship Manager. Express genuine care for their satisfaction and surface unresolved pain points.
            </div>
        </div>
        <div class="action-card">
            <div class="action-card-header">
                <div class="action-card-icon" style="background:linear-gradient(135deg,#0EA5E9 0%,#0284C7 100%); color:#FFFFFF; box-shadow:0 2px 8px rgba(14,165,233,0.25);">🎁</div>
                <div class="action-card-title">Personalised Retention Package</div>
            </div>
            <div style="font-size:0.84rem; color:#334155; line-height:1.55; padding-left:3.2rem;">
                Propose a tailored bundle — fee waivers, preferential interest rates, or upgraded card tier — calibrated to customer tenure and holdings.
            </div>
        </div>
        <div class="action-card">
            <div class="action-card-header">
                <div class="action-card-icon" style="background:linear-gradient(135deg,#A855F7 0%,#7E22CE 100%); color:#FFFFFF; box-shadow:0 2px 8px rgba(168,85,247,0.25);">👔</div>
                <div class="action-card-title">Assign Dedicated Senior Manager</div>
            </div>
            <div style="font-size:0.84rem; color:#334155; line-height:1.55; padding-left:3.2rem;">
                Pair the customer with a senior relationship manager for a comprehensive portfolio health check within the current business week.
            </div>
        </div>
        <div class="action-card">
            <div class="action-card-header">
                <div class="action-card-icon" style="background:linear-gradient(135deg,#10B981 0%,#059669 100%); color:#FFFFFF; box-shadow:0 2px 8px rgba(16,185,129,0.25);">📋</div>
                <div class="action-card-title">Complaint &amp; Service Review</div>
            </div>
            <div style="font-size:0.84rem; color:#334155; line-height:1.55; padding-left:3.2rem;">
                Audit last 90 days of support tickets and transaction friction to resolve open issues on an expedited basis.
            </div>
        </div>
        """

        impact_card = """
        <div class="insight-card insight-card-red" style="margin:0;">
            <div class="insight-card-icon">📈</div>
            <div style="flex:1;">
                <div class="insight-card-title">Business Impact — High Value at Stake</div>
                <div class="insight-card-body">
                    This customer sits in the <b>high-risk tier</b> with a strong predicted probability of churn.
                    Industry benchmarks indicate that <b>immediate, personalized intervention</b>
                    can improve retention likelihood by up to <b>35–50%</b> in comparable banking cohorts.
                    <br><br>
                    If account balance is high, prioritize senior retention budget and executive outreach.
                </div>
            </div>
        </div>
        """

    elif probability >= 0.30:

        st.markdown(
            """
            <div style="background:#FFFBEB; border:1px solid #FDE68A; border-radius:14px; padding:1rem 1.35rem; margin-bottom:1rem; display:flex; align-items:flex-start; gap:0.85rem; box-shadow:0 4px 18px -2px rgba(245,158,11,0.05);">
                <div style="width:40px; height:40px; border-radius:10px; background:linear-gradient(135deg, #F59E0B 0%, #D97706 100%); color:#FFFFFF; display:flex; align-items:center; justify-content:center; font-size:1.15rem; flex-shrink:0; box-shadow:0 3px 10px rgba(245,158,11,0.28);">⚡</div>
                <div style="flex:1;">
                    <div style="font-size:0.74rem; font-weight:700; letter-spacing:0.06em; text-transform:uppercase; color:#92400E; margin-bottom:0.15rem;">Retention Priority</div>
                    <div style="font-size:1.1rem; font-weight:800; color:#78350F; line-height:1.2;">Monitor &amp; Proactively Engage · Priority 2 Account</div>
                    <div style="font-size:0.84rem; color:#92400E; margin-top:0.2rem; line-height:1.45;">Moderate churn signal. Nudge and targeted marketing engagement recommended.</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        actions_html = """
        <div class="action-card">
            <div class="action-card-header">
                <div class="action-card-icon" style="background:linear-gradient(135deg,#0EA5E9 0%,#0284C7 100%); color:#FFFFFF; box-shadow:0 2px 8px rgba(14,165,233,0.25);">💌</div>
                <div class="action-card-title">Personalised Offers &amp; Communication</div>
            </div>
            <div style="font-size:0.84rem; color:#334155; line-height:1.55; padding-left:3.2rem;">
                Run a segmented offer: pre-approved card perks, bonus cashback, or discounted product bundles delivered via their preferred digital channel.
            </div>
        </div>
        <div class="action-card">
            <div class="action-card-header">
                <div class="action-card-icon" style="background:linear-gradient(135deg,#10B981 0%,#059669 100%); color:#FFFFFF; box-shadow:0 2px 8px rgba(16,185,129,0.25);">📊</div>
                <div class="action-card-title">Activity &amp; Engagement Monitoring</div>
            </div>
            <div style="font-size:0.84rem; color:#334155; line-height:1.55; padding-left:3.2rem;">
                Track monthly logins, transaction frequency, and digital banking visits. Flag any downward trends within 14 days.
            </div>
        </div>
        <div class="action-card">
            <div class="action-card-header">
                <div class="action-card-icon" style="background:linear-gradient(135deg,#A855F7 0%,#7E22CE 100%); color:#FFFFFF; box-shadow:0 2px 8px rgba(168,85,247,0.25);">📦</div>
                <div class="action-card-title">Recommend Additional Products</div>
            </div>
            <div style="font-size:0.84rem; color:#334155; line-height:1.55; padding-left:3.2rem;">
                Cross-sell into multi-product relationships (savings deposit, secondary card, investments) to deepen customer stickiness.
            </div>
        </div>
        """

        impact_card = """
        <div class="insight-card insight-card-amber" style="margin:0;">
            <div class="insight-card-icon">📈</div>
            <div style="flex:1;">
                <div class="insight-card-title">Business Impact — High Retention Leverage</div>
                <div class="insight-card-body">
                    Medium-risk accounts represent the <b>highest retention ROI</b>.
                    These customers are highly responsive to proactive engagement and value additions,
                    preventing drift into the high-risk churn tier.
                </div>
            </div>
        </div>
        """

    else:

        st.markdown(
            """
            <div style="background:#ECFDF5; border:1px solid #A7F3D0; border-radius:14px; padding:1rem 1.35rem; margin-bottom:1rem; display:flex; align-items:flex-start; gap:0.85rem; box-shadow:0 4px 18px -2px rgba(16,185,129,0.05);">
                <div style="width:40px; height:40px; border-radius:10px; background:linear-gradient(135deg, #10B981 0%, #059669 100%); color:#FFFFFF; display:flex; align-items:center; justify-content:center; font-size:1.15rem; flex-shrink:0; box-shadow:0 3px 10px rgba(16,185,129,0.28);">✅</div>
                <div style="flex:1;">
                    <div style="font-size:0.74rem; font-weight:700; letter-spacing:0.06em; text-transform:uppercase; color:#065F46; margin-bottom:0.15rem;">Retention Priority</div>
                    <div style="font-size:1.1rem; font-weight:800; color:#064E3B; line-height:1.2;">Customer Stable · Grow Customer Lifetime Value</div>
                    <div style="font-size:0.84rem; color:#065F46; margin-top:0.2rem; line-height:1.45;">Healthy retention signals. Focus on wallet-share, cross-sell, and loyalty advocacy.</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        actions_html = """
        <div class="action-card">
            <div class="action-card-header">
                <div class="action-card-icon" style="background:linear-gradient(135deg,#10B981 0%,#059669 100%); color:#FFFFFF; box-shadow:0 2px 8px rgba(16,185,129,0.25);">🤝</div>
                <div class="action-card-title">Sustain Regular Engagement</div>
            </div>
            <div style="font-size:0.84rem; color:#334155; line-height:1.55; padding-left:3.2rem;">
                Maintain value-add digital touches — quarterly account health summaries, market updates, and exclusive perks.
            </div>
        </div>
        <div class="action-card">
            <div class="action-card-header">
                <div class="action-card-icon" style="background:linear-gradient(135deg,#A855F7 0%,#7E22CE 100%); color:#FFFFFF; box-shadow:0 2px 8px rgba(168,85,247,0.25);">💎</div>
                <div class="action-card-title">Recommend Premium Tiers</div>
            </div>
            <div style="font-size:0.84rem; color:#334155; line-height:1.55; padding-left:3.2rem;">
                Explore wealth management, private banking, or premium credit card upgrades to maximize customer lifetime value.
            </div>
        </div>
        <div class="action-card">
            <div class="action-card-header">
                <div class="action-card-icon" style="background:linear-gradient(135deg,#0EA5E9 0%,#0284C7 100%); color:#FFFFFF; box-shadow:0 2px 8px rgba(14,165,233,0.25);">📈</div>
                <div class="action-card-title">Wealth &amp; Investment Solutions</div>
            </div>
            <div style="font-size:0.84rem; color:#334155; line-height:1.55; padding-left:3.2rem;">
                Propose tailored retirement plans or diversified structured investment vehicles aligned to customer financial capacity.
            </div>
        </div>
        """

        impact_card = """
        <div class="insight-card insight-card-green" style="margin:0;">
            <div class="insight-card-icon">📈</div>
            <div style="flex:1;">
                <div class="insight-card-title">Business Impact — Lifetime Value Growth</div>
                <div class="insight-card-body">
                    This customer shows a <b>strong retention profile</b>.
                    Rather than defensive retention expenditure, focus on <b>growing Customer Lifetime Value</b> (CLV)
                    and identifying candidates for brand advocacy and referral programs.
                </div>
            </div>
        </div>
        """

    col_actions, col_impact = st.columns([3, 2])

    with col_actions:
        st.markdown(
            """
            <div style="margin-bottom:0.6rem;">
                <span class="pill pill-blue" style="font-size:0.72rem; margin-bottom:0.25rem;">
                    <span>📋</span><span>Recommended Actions</span>
                </span>
                <div style="font-size:0.82rem; color:#64748B; margin-top:0.25rem;">
                    Targeted playbook actions ordered by retention impact.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(actions_html, unsafe_allow_html=True)

    with col_impact:
        st.markdown(
            """
            <div style="margin-bottom:0.6rem;">
                <span class="pill pill-purple" style="font-size:0.72rem; margin-bottom:0.25rem;">
                    <span>💡</span><span>Business Impact</span>
                </span>
                <div style="font-size:0.82rem; color:#64748B; margin-top:0.25rem;">
                    Strategic expected outcome for this account tier.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(impact_card, unsafe_allow_html=True)
