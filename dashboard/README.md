# 🏦 Bank Churn Intelligence Dashboard Documentation

This directory contains the multi-page Streamlit web application for the **Bank Customer Churn Prediction and Risk Intelligence Platform**.

---

## 🧭 Page Architecture & Navigation

The dashboard is structured into 6 focused pages:

1. **[app.py](file:///c:/Users/pradi/OneDrive/Desktop/Unified%20Mentor%20Project/v2/dashboard/app.py) — Central Command Hub & Real-time Risk Scorer**
   - Brand hero header with active model indicators.
   - Top-level model KPIs and champion benchmark card.
   - Real-time customer risk scoring with instant preset selection.
   - 3-tier risk banner, percentile cohort distribution marker, actionable playbooks, profile snapshot, and feature drivers.

2. **[Executive_Dashboard.py](file:///c:/Users/pradi/OneDrive/Desktop/Unified%20Mentor%20Project/v2/dashboard/pages/Executive_Dashboard.py) — Portfolio Health & Executive KPIs**
   - High-level customer portfolio statistics (total accounts, churn rate, active/inactive proportions, average balance).
   - Donut visualizers for customer status and churn share.
   - Dynamic data-driven strategic recommendations for management.
   - Model benchmark cards for quarterly stakeholder reporting.

3. **[Analytics.py](file:///c:/Users/pradi/OneDrive/Desktop/Unified%20Mentor%20Project/v2/dashboard/pages/Analytics.py) — Exploratory Analysis & Churn Drivers**
   - Demographics tab: Geography, Age, Credit Score, Tenure, and Estimated Salary histograms.
   - Product holdings analysis: Balance distributions, active membership, credit card ownership, and product count comparisons.
   - Bivariate churn segmentation bar charts and Pearson correlation heatmap.

4. **[Prediction.py](file:///c:/Users/pradi/OneDrive/Desktop/Unified%20Mentor%20Project/v2/dashboard/pages/Prediction.py) — Prediction Studio**
   - **Tab 1**: Single Customer Risk Calculator with 4 realistic preset profiles.
   - **Tab 2**: High-throughput **Batch CSV Scoring Engine** — upload custom CSV, score hundreds of accounts at once, view risk tier breakdown, and download scored CSV report.
   - **Tab 3**: Quick What-If sensitivity lever testing.
   - **Tab 4**: Operational Risk Framework & SLA Playbooks.

5. **[Explainability.py](file:///c:/Users/pradi/OneDrive/Desktop/Unified%20Mentor%20Project/v2/dashboard/pages/Explainability.py) — Model Explainability Suite (XAI)**
   - Global Gini and SHAP feature importance rankings.
   - SHAP summary beeswarm plot across the 2,000-record hold-out set.
   - Interactive SHAP dependence plots with automated interaction feature selection.
   - Local SHAP waterfall diagrams explaining single-customer decisions.

6. **[What_If_Simulator.py](file:///c:/Users/pradi/OneDrive/Desktop/Unified%20Mentor%20Project/v2/dashboard/pages/What_If_Simulator.py) — Retention Scenario Sandbox**
   - Step-by-step 3-stage retention simulator.
   - Baseline customer definition with 11 adjustable levers.
   - Real-time probability delta tracking, relative % shift, and tier migration indicators.

7. **[About_Project.py](file:///c:/Users/pradi/OneDrive/Desktop/Unified%20Mentor%20Project/v2/dashboard/pages/About_Project.py) — Specs & Developer Information**
   - End-to-end machine learning pipeline architecture.
   - Technology stack and library specifications.
   - Academic and developer credentials.

---

## 🎨 Design System

- **Typography**: Inter (Google Fonts) with smooth sub-pixel antialiasing.
- **Colorway**:
  - Primary Navy: `#0F172A` / `#1E40AF`
  - Accent Electric Blue: `#3B82F6`
  - Success Emerald: `#059669`
  - Warning Amber: `#D97706`
  - Danger Crimson: `#DC2626`
  - Purple (XAI): `#7C3AED`
- **Theme**: Light glassmorphic surface cards (`backdrop-filter: blur(14px)`), subtle borders (`#E2E8F0`), micro-animations, and hover lift effects.
