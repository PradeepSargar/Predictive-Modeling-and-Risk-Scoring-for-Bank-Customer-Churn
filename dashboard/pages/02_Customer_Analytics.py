import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st

from components.theme import apply_global_theme
from components.sidebar import display_sidebar
from components.header import display_brand_header
from components.section_header import display_section_header
from components.kpi_card import render_kpi_row

from services.data_service import DataService
from components.geography_chart import display_geography_chart
from components.active_member_chart import display_active_member_chart
from components.churn_distribution_chart import display_churn_distribution_chart
from components.balance_distribution_chart import display_balance_distribution_chart
from components.age_distribution_chart import display_age_distribution_chart
from components.credit_score_distribution_chart import display_credit_score_distribution_chart
from components.geography_vs_churn_chart import display_geography_vs_churn_chart
from components.active_member_vs_churn_chart import display_active_member_vs_churn_chart
from components.gender_vs_churn_chart import display_gender_vs_churn_chart
from components.products_vs_churn_chart import display_products_vs_churn_chart
from components.credit_card_vs_churn_chart import display_credit_card_vs_churn_chart
from components.tenure_distribution_chart import display_tenure_distribution_chart
from components.salary_distribution_chart import display_salary_distribution_chart
from components.correlation_heatmap import display_correlation_heatmap

st.set_page_config(
    page_title="Customer Analytics | Bank Churn Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_global_theme()
display_sidebar()

display_brand_header(
    title="Customer Analytics",
    subtitle="Exploratory customer intelligence — demographic profiles, engagement patterns, behavioral drivers, and segment attrition rates.",
    badges=[
        ("📊", "10,000 Customers"),
        ("🌍", "3 Countries · France · Spain · Germany"),
        ("📈", "15+ Visual Analytics Modules"),
        ("🎯", "Segment Churn Drivers"),
    ],
    icon="📊",
)

df = DataService.load_dataset()

summary = DataService.get_cohort_summary(df)
total_customers = summary["total_customers"]
churn_count = summary["churned_customers"]
churn_rate = summary["churn_rate"]
total_balance = df["Balance"].sum() if "Balance" in df.columns else 0.0
avg_balance = summary["average_balance"]
avg_credit = summary["average_credit_score"]
active_count = summary["active_customers"]
inactive_count = total_customers - active_count
card_holders = int(df["HasCrCard"].sum()) if "HasCrCard" in df.columns else 0

# Top Portfolio KPI Strip
summary_cards = [
    {"title": "Total Customers", "value": f"{total_customers:,}", "icon": "👥", "variant": "blue",
     "subtitle": "European retail accounts"},
    {"title": "Cohort Churn Rate", "value": f"{churn_rate:.2f}%", "icon": "📉", "variant": "red",
     "subtitle": f"{churn_count:,} churned accounts"},
    {"title": "Aggregate AUM", "value": f"${total_balance:,.0f}", "icon": "💰", "variant": "green",
     "subtitle": "Total customer deposits"},
    {"title": "Avg. Customer Balance", "value": f"${avg_balance:,.0f}", "icon": "🏦", "variant": "purple",
     "subtitle": "Per-customer mean AUM"},
]
render_kpi_row(summary_cards, cols=4)

st.markdown('<div style="height:0.25rem;"></div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Structured 4-Tab Analytics Architecture
# -----------------------------------------------------------------------------
tab_profile, tab_behavior, tab_churn, tab_relations = st.tabs([
    "👤 Tab 1: Customer Profile",
    "⚡ Tab 2: Customer Behavior",
    "📉 Tab 3: Churn Analysis",
    "🔗 Tab 4: Relationships & Correlation",
])

# =============================================================================
# TAB 1: CUSTOMER PROFILE (Symmetrical 2-Column Pairs with Section Dividers)
# =============================================================================
with tab_profile:
    display_section_header(
        "Demographic & Financial Footprint",
        "Geographic concentration, age distribution, balance levels, and customer relationship tenure.",
        accent_color="#0EA5E9",
    )

    # Subsection 1: Regional & Age Demographics
    st.markdown(
        """
        <div class="graph-group-header">
            <span class="graph-group-badge">Region &amp; Age</span>
            <span class="graph-group-title">Demographics &amp; Geographical Footprint</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    col_p1, col_p2 = st.columns(2, gap="medium")
    with col_p1:
        display_geography_chart(df, key="tab1_geography")
    with col_p2:
        display_age_distribution_chart(df, key="tab1_age")

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # Subsection 2: Balances & Salaries
    st.markdown(
        """
        <div class="graph-group-header">
            <span class="graph-group-badge">Balances &amp; Salary</span>
            <span class="graph-group-title">Financial Position &amp; Wealth Distribution</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    col_p3, col_p4 = st.columns(2, gap="medium")
    with col_p3:
        display_balance_distribution_chart(df, key="tab1_balance")
    with col_p4:
        display_salary_distribution_chart(df, key="tab1_salary")

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # Subsection 3: Credit Scores & Tenure
    st.markdown(
        """
        <div class="graph-group-header">
            <span class="graph-group-badge">Credit &amp; Tenure</span>
            <span class="graph-group-title">Credit Standing &amp; Relationship Length</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    col_p5, col_p6 = st.columns(2, gap="medium")
    with col_p5:
        display_credit_score_distribution_chart(df, key="tab1_credit")
    with col_p6:
        display_tenure_distribution_chart(df, key="tab1_tenure")

# =============================================================================
# TAB 2: CUSTOMER BEHAVIOR (Engagement & Product Holdings with Dividers)
# =============================================================================
with tab_behavior:
    display_section_header(
        "Product Ownership & Engagement Behavior",
        "Analysis of active digital banking usage, product bundle counts, and credit card penetration.",
        accent_color="#A855F7",
    )

    # Behavior KPI Summary
    behavior_kpis = [
        {"title": "Active Digital Members", "value": f"{active_count:,}", "icon": "⚡", "variant": "green",
         "subtitle": f"{active_count / total_customers * 100:.1f}% engagement rate"},
        {"title": "Inactive Accounts", "value": f"{inactive_count:,}", "icon": "⚠️", "variant": "amber",
         "subtitle": f"{inactive_count / total_customers * 100:.1f}% dormant accounts"},
        {"title": "Credit Card Holders", "value": f"{card_holders:,}", "icon": "💳", "variant": "blue",
         "subtitle": f"{card_holders / total_customers * 100:.1f}% card penetration"},
        {"title": "Avg Products / Customer", "value": f"{df['NumOfProducts'].mean():.2f}", "icon": "📦", "variant": "purple",
         "subtitle": "Mean bundle depth"},
    ]
    render_kpi_row(behavior_kpis, cols=4)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # Subsection 1: Activity & Credit Cards
    st.markdown(
        """
        <div class="graph-group-header">
            <span class="graph-group-badge">Digital &amp; Cards</span>
            <span class="graph-group-title">Channel Activity &amp; Payment Card Penetration</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    col_b1, col_b2 = st.columns(2, gap="medium")
    with col_b1:
        display_active_member_chart(df, key="tab2_active_member")
    with col_b2:
        display_credit_card_vs_churn_chart(df, key="tab2_credit_card_churn")

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # Subsection 2: Product Holdings & Strategic Insights
    st.markdown(
        """
        <div class="graph-group-header">
            <span class="graph-group-badge">Bundles &amp; Loyalty</span>
            <span class="graph-group-title">Product Depth &amp; Churn Sensitivity</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    col_b3, col_b4 = st.columns(2, gap="medium")
    with col_b3:
        display_products_vs_churn_chart(df, key="tab2_products_churn")
    with col_b4:
        st.markdown(
            """
            <div class="card-surface card-gradient-purple" style="height:100%;">
                <div class="card-header">
                    <div class="card-icon card-icon-purple">📦</div>
                    <div>
                        <div class="card-title">Behavioral Patterns</div>
                        <h3 style="margin:0; font-size:1.05rem; color:#0F172A;">Product & Engagement Dynamics</h3>
                    </div>
                </div>
                <div style="font-size:0.86rem; color:#334155; line-height:1.65; margin-top:0.6rem;">
                    • <b>Optimal Product Depth (2 Products)</b>: Customers holding exactly 2 banking products exhibit the lowest churn rate (< 8%), representing the bank's most loyal and sticky relationship tier.<br><br>
                    • <b>Single Product Risk (1 Product)</b>: Customers with only 1 product account for over 50% of the customer base and experience an elevated ~27.7% churn rate.<br><br>
                    • <b>Over-saturation Fatigue (3–4 Products)</b>: Clients with 3 or 4 products have an extreme churn rate (> 80%), indicating potential product mismatch, high fees, or complex account maintenance friction.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# =============================================================================
# TAB 3: CHURN ANALYSIS (Symmetrical Attrition Breakdown with Dividers)
# =============================================================================
with tab_churn:
    display_section_header(
        "Cohort Churn Breakdown & Segment Attrition",
        "Granular churn distributions comparing attrition rates across geography, gender, age, and activity status.",
        accent_color="#EF4444",
    )

    # Subsection 1: Macro Split & Country
    st.markdown(
        """
        <div class="graph-group-header">
            <span class="graph-group-badge">Macro &amp; Country</span>
            <span class="graph-group-title">Portfolio Attrition Split &amp; Country Breakdown</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    col_c1, col_c2 = st.columns(2, gap="medium")
    with col_c1:
        display_churn_distribution_chart(df, key="tab3_churn_donut")
    with col_c2:
        display_geography_vs_churn_chart(df, key="tab3_geography_churn")

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # Subsection 2: Gender & Activity
    st.markdown(
        """
        <div class="graph-group-header">
            <span class="graph-group-badge">Demographic &amp; Activity</span>
            <span class="graph-group-title">Gender &amp; Digital Membership Attrition Drivers</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    col_c3, col_c4 = st.columns(2, gap="medium")
    with col_c3:
        display_gender_vs_churn_chart(df, key="tab3_gender_churn")
    with col_c4:
        display_active_member_vs_churn_chart(df, key="tab3_active_churn")

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # Subsection 3: Product Holding Churn & Segment Strategy
    st.markdown(
        """
        <div class="graph-group-header">
            <span class="graph-group-badge">Product Holding Risk</span>
            <span class="graph-group-title">Product Holding Risk &amp; Concentration Takeaways</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    col_c5, col_c6 = st.columns(2, gap="medium")
    with col_c5:
        display_products_vs_churn_chart(df, key="tab3_products_churn")
    with col_c6:
        st.markdown(
            """
            <div class="card-surface card-gradient-red" style="height:100%;">
                <div class="card-header">
                    <div class="card-icon card-icon-red">🎯</div>
                    <div>
                        <div class="card-title">Attrition Concentration</div>
                        <h3 style="margin:0; font-size:1.05rem; color:#0F172A;">Highest Risk Customer Pockets</h3>
                    </div>
                </div>
                <div style="font-size:0.86rem; color:#334155; line-height:1.65; margin-top:0.6rem;">
                    • <b>German Regional Concentration</b>: German accounts exhibit a 32.4% churn rate — double that of France (16.2%) and Spain (16.7%).<br><br>
                    • <b>Gender Attrition Disparity</b>: Female accounts churn at 25.1% vs 16.5% for male accounts, representing a key focus area for customer journey audits.<br><br>
                    • <b>Inactivity Multiplier</b>: Inactive members are nearly 2× more likely to leave the bank (26.8% vs 14.3% for actively engaged customers).
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# =============================================================================
# TAB 4: RELATIONSHIPS & CORRELATION
# =============================================================================
with tab_relations:
    display_section_header(
        "Feature Relationship Matrix & Key Churn Drivers",
        "Pearson correlation matrix revealing co-linear variables and primary risk drivers.",
        accent_color="#F59E0B",
    )

    st.markdown(
        """
        <div class="graph-group-header">
            <span class="graph-group-badge">Correlation Matrix</span>
            <span class="graph-group-title">Pearson Linear Feature Dependencies</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    display_correlation_heatmap(df, key="tab4_correlation_heatmap")

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="graph-group-header">
            <span class="graph-group-badge">Insights &amp; Strategy</span>
            <span class="graph-group-title">Executive Takeaways &amp; Operational Priorities</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_r1, col_r2 = st.columns(2, gap="medium")
    with col_r1:
        st.markdown(
            """
            <div class="card-surface card-gradient-amber" style="height:100%;">
                <div class="card-header">
                    <div class="card-icon card-icon-amber">💡</div>
                    <div>
                        <div class="card-title">Correlation Findings</div>
                        <h3 style="margin:0; font-size:1.02rem; color:#0F172A;">Key Statistical Drivers</h3>
                    </div>
                </div>
                <div style="font-size:0.86rem; color:#334155; line-height:1.65; margin-top:0.6rem;">
                    • <b>Age Correlation (r = +0.29)</b>: Age shows the strongest positive correlation with churn among all single variables.<br>
                    • <b>Activity Status (r = -0.16)</b>: Active membership exhibits the strongest protective (negative) correlation against churn.<br>
                    • <b>Balance & Country (r = +0.40)</b>: German accounts hold significantly higher mean balances than French or Spanish accounts.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col_r2:
        st.markdown(
            """
            <div class="card-surface card-gradient-blue" style="height:100%;">
                <div class="card-header">
                    <div class="card-icon card-icon-blue">🧭</div>
                    <div>
                        <div class="card-title">Operational Action Items</div>
                        <h3 style="margin:0; font-size:1.02rem; color:#0F172A;">Targeted Retention Priorities</h3>
                    </div>
                </div>
                <div style="font-size:0.86rem; color:#334155; line-height:1.65; margin-top:0.6rem;">
                    • <b>Re-engagement Campaign</b>: Launch automated nudges and digital banking onboarding for inactive accounts.<br>
                    • <b>Dual-Product Bundle</b>: Encourage 1-product holders to adopt a high-yield savings or credit card account.<br>
                    • <b>Wealth Retention in Germany</b>: Dedicated relationship manager touchpoints for German accounts with balances > $100k.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
