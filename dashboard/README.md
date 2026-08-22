# 🏦 Bank Churn Intelligence Dashboard Architecture

This directory contains the multi-page Streamlit web application for the **Bank Customer Churn Prediction and Risk Intelligence Platform**.

---

## 🧭 Page Architecture & Navigation (8-Page Multi-Page Suite)

The dashboard is structured into 8 modular, enterprise-grade pages:

1. **`app.py` — Central Command Hub & Real-Time Executive Scorer**
   - Brand hero banner with active model status badges.
   - Top-level model KPIs and champion benchmark cards.
   - Real-time customer intake form with 1-click risk personas.
   - 3-tier risk banner, percentile cohort distribution marker, actionable playbooks, profile snapshot, and feature drivers.

2. **`01_Executive_Overview.py` — Portfolio Health & C-Suite KPIs**
   - High-level customer portfolio metrics (Total Accounts, Churn Rate, Active Proportions, Average Balance, Value-at-Risk).
   - Donut visualizers for customer distribution and churn proportion.
   - Executive strategic recommendations with priority SLAs.
   - Model benchmark cards for stakeholder reporting.

3. **`02_Customer_Analytics.py` — Exploratory Analysis & Demographic Footprint**
   - **Demographics Tab**: Geography, Age, Credit Score, Tenure, and Estimated Salary distributions.
   - **Customer Behavior Tab**: Digital engagement, payment card penetration, and product depth analysis.
   - **Bivariate Churn Drivers Tab**: Cross-segmentation comparisons, Pearson correlation heatmap, and key business takeaways.

4. **`03_Risk_Portfolio.py` — Customer Triage & Value-at-Risk Priority Queue**
   - 9-lever interactive customer cohort filtering sandbox (Geography, Products, Active status, Balance, Age, Probability range).
   - Value-at-Risk proxy calculations (`Balance × Churn Probability`) highlighting high-exposure accounts.
   - Germany market strategic intervention playbook.
   - Exportable filtered customer retention priority queue (CSV).

5. **`04_Model_Performance.py` — 5-Fold Stratified Cross-Validation & Decision Calibration**
   - 5-Model comparative benchmark table with mean ± standard deviation across Accuracy, ROC-AUC, Precision, Recall, and F1.
   - Visual performance benchmarks across candidate algorithms.
   - Interactive Holdout Confusion Matrix comparison (Default 0.50 Mode vs. Selected 0.35 Retention Policy).
   - Out-of-Fold (OOF) decision threshold optimization curve.

6. **`05_Model_Explainability.py` — Explainable AI (XAI) Suite**
   - Global Gini and SHAP feature importance rankings.
   - SHAP summary beeswarm plot across the 2,000-record holdout test cohort.
   - Interactive SHAP dependence plots with automated non-linear interaction feature selection.
   - Local SHAP waterfall attribution diagrams explaining individual customer predictions.
   - Multi-feature Partial Dependence Plots (PDP) showing non-linear inflection thresholds.

7. **`06_Customer_Risk_Scoring.py` — Real-Time Scoring Studio & Batch Engine**
   - **Individual Intake Tab**: Parameter intake form, 1-click persona presets, operating threshold selector (0.20, 0.35, 0.50), probability gauge, and 1-page printable Customer Retention Brief dossier export.
   - **Batch CSV Scoring Tab**: High-throughput batch inference engine with CSV upload, sample data scoring, and enriched risk score report download.
   - **Risk Framework Tab**: 3-tier risk hierarchy and SLA intervention protocols.

8. **`07_Scenario_Simulator.py` — What-If Retention Simulation Sandbox**
   - 3-stage interactive what-if retention simulator.
   - Baseline customer definition with 11 adjustable parameters.
   - Real-time probability delta tracking, relative risk mitigation %, and Customer Lifetime Value (CLV) deposit balance protection ROI calculation.

9. **`08_Platform_Overview.py` — Enterprise Architecture & Governance**
   - 16-step end-to-end analytical pipeline blueprint.
   - Complete technology stack and library specifications.
   - Academic, institutional, and developer credentials.

---

## 🎨 Enterprise Design System

- **Typography**: Inter (Google Fonts) with crisp sub-pixel antialiasing.
- **Palette**:
  - Primary Sky: `#0EA5E9` / `#0284C7`
  - Success Emerald: `#10B981` / `#059669`
  - Warning Amber: `#F59E0B` / `#D97706`
  - Danger Rose: `#EF4444` / `#DC2626`
  - Purple (XAI): `#A855F7` / `#7E22CE`
- **UI Components**:
  - Glassmorphic surface cards with border radius (`14px`) and subtle drop shadows.
  - Symmetrical responsive grid layouts.
  - Zero-scrollbar Plotly visualization cards with top-right 1-click fullscreen expansion.

