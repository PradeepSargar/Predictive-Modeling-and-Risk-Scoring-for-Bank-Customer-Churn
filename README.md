# 🏦 Bank Customer Churn Intelligence & Risk Platform
### *Enterprise-Grade Predictive Analytics, Risk Scoring & Decision Optimization Suite*

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Scikit-Learn](https://img.shields.io/badge/scikit_learn-1.3+-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![XGBoost](https://img.shields.io/badge/XGBoost-2.0+-EB4034?style=for-the-badge&logo=xgboost&logoColor=white)](https://xgboost.readthedocs.io)
[![SHAP](https://img.shields.io/badge/SHAP-Explainable_AI-7C3AED?style=for-the-badge)](https://shap.readthedocs.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

---

## 📑 Table of Contents
- [Executive Overview](#-executive-overview)
- [Key Business Metrics & Problem Statement](#-key-business-metrics--problem-statement)
- [Exploratory Data Analytics (EDA) Insights](#-exploratory-data-analytics-eda-insights)
- [Machine Learning Architecture & Validation](#-machine-learning-architecture--validation)
- [Decision Threshold Optimization](#-decision-threshold-optimization)
- [Value-at-Risk (VAR) & Retention Matrix](#-value-at-risk-var--retention-matrix)
- [Explainable AI (XAI) with SHAP](#-explainable-ai-xai-with-shap)
- [Multi-Page Streamlit Dashboard Suite](#-multi-page-streamlit-dashboard-suite)
- [System Architecture & Directory Layout](#-system-architecture--directory-layout)
- [How to Run the Project (Getting Started)](#-how-to-run-the-project-getting-started)
- [Actionable Business Recommendations](#-actionable-business-recommendations)
- [Author & Project Credits](#-author--project-credits)

---

## 🎯 Executive Overview

In the commercial and retail banking sectors, customer acquisition costs **5× to 25× more** than retaining existing depositors. When high-balance account holders churn, institutions lose not only recurring fee revenues but also foundational loan-capital liquidity.

This platform bridges the gap between **advanced predictive modeling** and **commercial decision-making**. It transitions banking institutions from reactive post-exit reporting to **proactive, real-time risk triage and intervention**.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                 CORE VALUE DELIVERABLES                                │
├──────────────────────────┬──────────────────────────┬──────────────────────────────────┤
│   🎯 87.08% ROC-AUC      │   🛡️ 5-Fold Stratified   │   💼 +22.6% Churn Catch Gain     │
│   Champion GB Classifier │   Leakage-Free Validation│   via 0.35 Decision Threshold    │
├──────────────────────────┼──────────────────────────┼──────────────────────────────────┤
│   🔍 SHAP Game Theory    │   💰 Value-at-Risk (VAR) │   🖥️ 8-Page Glassmorphic         │
│   Local & Global XAI     │   Capital Exposure Triage│   Streamlit Analytics Suite      │
└──────────────────────────┴──────────────────────────┴──────────────────────────────────┘
```

---

## 💼 Key Business Metrics & Problem Statement

### The Business Challenge
- **Portfolio Scale**: 10,000 European retail banking accounts across France, Germany, and Spain.
- **Baseline Churn Rate**: **20.37%** (2,037 accounts lost; 7,963 retained).
- **Core Objective**: Accurately predict account attrition, discover non-linear behavioral drivers, audit individual risk scores via Explainable AI, and optimize intervention economics.

### High-Level Portfolio Baseline
| Portfolio Metric | Value | Business Context |
| :--- | :---: | :--- |
| **Total Analyzed Cohort** | `10,000` | European retail banking accounts |
| **Total Churned Depositors** | `2,037` | **20.37%** historical cohort attrition rate |
| **Active Member Ratio** | `51.51%` | 5,151 active vs 4,849 inactive accounts |
| **Average Account Balance** | `€76,485.88` | Liquid deposit baseline per customer |
| **Average Credit Score** | `650.53` | Median FICO creditworthiness grade |
| **Estimated Total Value-at-Risk** | `€155.8M+` | Cumulative capital exposure in at-risk balances |

---

## 📊 Exploratory Data Analytics (EDA) Insights

Thorough exploratory data analysis revealed several critical non-linear behavioral patterns that direct retention strategies:

### 1. Geographic Disparity (The Germany Inflection)
- **Germany**: Accounts churn at **32.44%** — more than **double** France (`16.15%`) and Spain (`16.67%`).
- *Root Driver*: German account holders maintain significantly higher average balances (`€119,730` avg vs `€62,094` in France) but exhibit lower cross-product loyalty.

### 2. The Product Paradox (Multi-Product Friction)
- **1 Product**: 27.71% churn rate (baseline risk).
- **2 Products**: **7.58% churn rate (Optimal Retention Zone ⭐)**.
- **3 Products**: **82.71% churn rate (Severe Risk ⚠️)**.
- **4 Products**: **100.00% churn rate (Extreme Risk 🚨)**.
- *Strategic Takeaway*: While a second product strengthens customer retention, holding 3 or 4 products creates friction, fee dissatisfaction, or operational complexity.

### 3. Engagement & Inactivity Impact
- **Inactive Members**: **26.85% churn** vs **14.27%** for active members (a **1.88× risk multiplier**).
- Digital and operational inactivity is the single fastest-growing leading indicator of churn.

### 4. Age Demographic Vulnerability
- Customers aged **45–60** exhibit the highest attrition rate (**~56%**), representing mature, high-net-worth professionals with portable wealth seeking competitive yields elsewhere.

---

## 🏆 Machine Learning Architecture & Validation

Five machine learning architectures were trained on 8,000 training records using **5-Fold Stratified Cross-Validation** and evaluated against an untouched 2,000-record holdout test cohort.

### 1. 5-Fold Stratified Cross-Validation Benchmark (8,000 Records)
*Evaluated across 5 validation folds to guarantee generalizability and rule out data leakage:*

| Model Architecture | Mean Accuracy $\pm$ Std | Mean Precision $\pm$ Std | Mean Recall $\pm$ Std | Mean F1-Score $\pm$ Std | Mean ROC-AUC $\pm$ Std | Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **🏆 Gradient Boosting** | **86.31% ± 0.99%** | **77.22% ± 3.17%** | **46.44% ± 3.56%** | **57.98% ± 3.65%** | **86.48% ± 0.95%** | **Champion** |
| **⚡ XGBoost** | 86.08% ± 0.79% | 75.55% ± 2.71% | 46.75% ± 2.55% | 57.75% ± 2.71% | 86.47% ± 0.96% | Alternative |
| **🌲 Random Forest** | 85.82% ± 0.84% | 74.60% ± 2.81% | 46.07% ± 2.75% | 56.96% ± 2.90% | 85.02% ± 1.22% | Benchmark |
| **📈 Logistic Regression** | 81.05% ± 0.67% | 59.67% ± 4.43% | 21.41% ± 2.58% | 31.48% ± 3.27% | 76.28% ± 1.93% | Baseline |
| **🌿 Decision Tree** | 78.69% ± 0.63% | 47.81% ± 1.44% | 50.18% ± 3.64% | 48.91% ± 2.15% | 68.08% ± 1.54% | Baseline |

### 2. Final Holdout Test Verification (2,000 Untouched Records)
| Model | Test Accuracy | Test Precision | Test Recall | Test F1-Score | Test ROC-AUC | Production Role |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **🏆 Gradient Boosting** | **87.00%** | **79.28%** | **48.89%** | **60.49%** | **87.08%** | **Production Champion** |
| **⚡ XGBoost** | 86.65% | 77.34% | 48.65% | 59.73% | 86.72% | Secondary Engine |
| **🌲 Random Forest** | 86.40% | 75.76% | 49.14% | 59.61% | 86.24% | Ensemble Baseline |
| **📈 Logistic Regression** | 80.80% | 58.91% | 18.67% | 28.36% | 77.48% | Linear Baseline |
| **🌿 Decision Tree** | 78.60% | 47.72% | 51.60% | 49.59% | 68.85% | Non-linear Baseline |

---

## 🎚️ Decision Threshold Optimization

Default classification models use a hardcoded threshold of $T = 0.50$, which is optimized for symmetric errors. However, in banking retention, **failing to flag a churner (False Negative) costs significantly more than contacting a loyal customer (False Positive)**.

Threshold calibration was performed strictly on **Out-Of-Fold (OOF) cross-validation predictions**:

```
                       THRESHOLD TRADE-OFF LANDSCAPE
  Threshold  Accuracy   Precision    Recall      F1-Score   Churners Caught   Strategic Objective
  ─────────────────────────────────────────────────────────────────────────────────────────────
    0.20      80.10%     50.80%     74.11%       60.28%     1,208 / 1,630     ⚡ Max Early Warning
    0.30      84.64%     62.01%     63.50%       62.75%     1,035 / 1,630     🔄 High-Coverage Nudges
  ⭐ 0.35      85.51%     66.23%     58.96%       62.38%       961 / 1,630     🎯 Optimal Retention Balance
    0.50      86.31%     77.32%     46.44%       58.03%       757 / 1,630     🛡️ Conservative Precision
```

### Unbiased Holdout Test Impact (2,000 Records):
- **Default Mode ($0.50$)**: Identifies 199 / 407 churners ($48.89\%$ recall).
- **Selected Policy ($0.35$)**: Identifies **244 / 407 churners ($59.95\%$ recall)**.
- **Net Gain**: **+45 additional at-risk depositors salvaged (+22.61% relative capture gain)**.
- **Economic Value**: In an illustrative retail bank scenario ($\text{CLV} = \$2,500$, save rate $= 25\%$, contact cost $= \$50$), switching to $0.35$ unlocks **+$22,375 in net added value** per 2,000 accounts.

---

## 💼 Value-at-Risk (VAR) & Retention Matrix

To ensure relationship managers focus their time where revenue loss is highest, the platform pairs model probabilities with a **Customer Value Proxy (CVP)**:

$$\text{CVP} = \text{Balance} + (0.5 \times \text{EstimatedSalary})$$

$$\text{Loss Exposure Index} = \text{CVP} \times \hat{P}(\text{Churn})$$

```
┌───────────────────────────────────────────────────────────────────────────────────────────┐
│                           4-TIER STRATEGIC RETENTION MATRIX                               │
├─────────────────────┬───────────────────────────┬─────────────────────────────────────────┤
│ Tier Category       │ Qualification Criteria    │ Prescribed Retention Playbook & SLA     │
├─────────────────────┼───────────────────────────┼─────────────────────────────────────────┤
│ 🔴 Critical         │ Churn Prob ≥ 70% AND      │ ⏱️ 24-Hour RM Executive Outreach        │
│    Priority         │ Top 30% Value (CVP)       │ Custom fee waiver & VIP concierge call  │
├─────────────────────┼───────────────────────────┼─────────────────────────────────────────┤
│ 🟠 High             │ Churn Prob ≥ 70% OR       │ ⏱️ 48-Hour Priority Account Review      │
│    Priority         │ Med Churn (30-70%) + High │ High-yield deposit lock & rate match    │
├─────────────────────┼───────────────────────────┼─────────────────────────────────────────┤
│ 🟡 Medium           │ Med Churn (30-70%) with   │ ⏱️ 7-Day Automated Digital Campaign     │
│    Priority         │ Low/Med Value (CVP)       │ Targeted product benefits & mobile app  │
├─────────────────────┼───────────────────────────┼─────────────────────────────────────────┤
│ 🟢 Low Priority     │ Churn Prob < 30%          │ ⏱️ Routine Relationship Maintenance     │
│    (Nurture)        │ Healthy Account Status    │ Cross-sell 2nd product (Optimal Zone)   │
└─────────────────────┴───────────────────────────┴─────────────────────────────────────────┘
```

---

## 🧠 Explainable AI (XAI) with SHAP

The platform implements game-theoretic **SHAP (SHapley Additive exPlanations)** to ensure full auditability and regulatory compliance (GDPR/EU AI Act aligned):

- **Global Feature Importance**: Identifies `Age`, `NumOfProducts`, `IsActiveMember`, `Geography_Germany`, and `Balance` as the top 5 macroeconomic drivers of customer departure.
- **SHAP Summary Beeswarm**: Shows exact directional impacts (e.g., high age pushes probability higher; active membership drives probability down).
- **SHAP Dependence Plots**: Captures non-linear thresholds and cross-feature interactions automatically.
- **Local Waterfall Attributions**: Step-by-step feature breakdown for any individual customer explaining how their score was built up from the cohort baseline.

---

## 🖥️ Multi-Page Streamlit Dashboard Suite

The application is architected as an 8-page, modern glassmorphic web platform:

```
dashboard/
├── app.py                      # 🌐 Central Command Hub & Real-time Risk Scorer
└── pages/
    ├── 01_Executive_Overview.py    # 📊 Portfolio Health, Churn KPIs & C-Suite Strategy
    ├── 02_Customer_Analytics.py    # 🔍 15+ Exploratory Visualizers & Demographic Maps
    ├── 03_Risk_Portfolio.py        # 🎯 Customer Triage Queue with Value-at-Risk Ranking
    ├── 04_Model_Performance.py     # 📈 5-Fold Cross-Validation & Decision Calibration Curves
    ├── 05_Model_Explainability.py  # 🧠 SHAP Beeswarm, Dependence & Waterfall Attributions
    ├── 06_Customer_Risk_Scoring.py # ⚡ Single Customer Scorer & Batch CSV Inference Engine
    ├── 07_Scenario_Simulator.py    # 🧪 What-If Retention Simulation & ROI Calculator
    └── 08_Platform_Overview.py     # 🏗️ System Architecture, Tech Stack & Governance
```

---

## 🏗️ System Architecture & Directory Layout

```
Predictive Modeling and Risk Scoring for Bank Customer Churn/
│
├── .streamlit/
│   └── config.toml                 # Streamlit theme, layout & server configuration
│
├── data/
│   ├── Processed/
│   │   └── customer_risk_report.csv # Engineered European bank cohort (10,000 records)
│   └── Raw/
│       └── European_Bank.csv        # Raw dataset source
│
├── models/
│   ├── gradient_boosting_model.pkl  # Champion trained Gradient Boosting classifier
│   ├── scaler.pkl                  # Fitted StandardScaler artifact
│   ├── label_encoder.pkl           # Label encoder mappings
│   ├── shap_explainer.pkl          # SHAP TreeExplainer model
│   ├── shap_values.pkl             # Precomputed SHAP attribution matrix
│   ├── feature_importance.pkl      # Global feature importance registry
│   ├── feature_names.pkl           # Feature name sequence
│   └── X_test.pkl                  # Holdout test cohort (2,000 records)
│
├── notebooks/
│   └── Bank_Churn_Analysis.ipynb   # 26-Section comprehensive ML research notebook
│
├── dashboard/                      # Multi-Page Streamlit Web Application
│   ├── app.py                      # Application entry point
│   ├── pages/                      # 8 Dedicated analytical modules
│   ├── components/                 # 25+ Glassmorphic Plotly & Streamlit UI widgets
│   ├── services/                   # Business logic, caching & inference layer
│   └── utils/                      # Styling palettes, validators & formatters
│
├── reports/
│   ├── Executive_Summary.pdf       # Formal C-Suite executive briefing
│   └── Research_Paper.pdf          # Full academic research methodology paper
│
├── requirements.txt                # Production dependency specification
├── LICENSE                         # MIT License
└── README.md                       # Master project documentation
```

---

## ⚡ How to Run the Project (Getting Started)

### 1. Prerequisites
- **Python**: Version `3.10` or higher (`Python 3.10`, `3.11`, `3.12`, or `3.13`)
- **Git**: For cloning the repository

---

### 2. Clone Repository & Setup Virtual Environment

```bash
# Clone repository
git clone https://github.com/PradeepSargar/Bank-Customer-Churn-Intelligence-Risk-Platform.git
cd "Predictive Modeling and Risk Scoring for Bank Customer Churn"
```

#### On Windows (PowerShell / Command Prompt):
```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment (PowerShell)
.\venv\Scripts\Activate.ps1
# OR (Command Prompt)
.\venv\Scripts\activate.bat
```

#### On macOS / Linux:
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

### 4. Launch the Streamlit Analytics Dashboard

```bash
python -m streamlit run dashboard/app.py
```
*(Alternatively: `streamlit run dashboard/app.py`)*

The multi-page application will launch automatically at:
👉 **`http://localhost:8501`**

---

### 5. Running the Research & ML Training Notebook

To inspect, run, or reproduce the end-to-end Machine Learning pipeline:

```bash
jupyter notebook notebooks/Bank_Churn_Analysis.ipynb
# or
jupyter lab
```

---

## 💡 Actionable Business Recommendations

1. **Activate the 2-Product Cross-Sell Strategy**:
   Customers holding exactly 2 products demonstrate an industry-low **7.58% churn rate**. Encourage single-product holders to adopt a linked savings or credit card product.
2. **Re-engineer Multi-Product Experience (3+ Products)**:
   Investigate fee structures and digital interfaces for 3- and 4-product holders where churn exceeds **80%**.
3. **Targeted Germany Regional Playbook**:
   Implement a customized competitive rate matching program for German branches where deposit attrition is 2× higher.
4. **Deploy the 0.35 Decision Threshold Policy**:
   Shift from passive 0.50 thresholding to active 0.35 retention mode to protect an estimated **+$22,375 net added value** per 2,000 customer accounts.

---

## 👨‍💻 Author & Project Credits

- **Author**: **Pradeep Sargar**
- **Degree**: Bachelor of Engineering (Computer Engineering)
- **Institution**: University of Mumbai
- **Domain Focus**: Applied Machine Learning, Risk Intelligence, Fintech Decision Platforms
- **Project Program**: Unified Mentor Advanced Analytics Internship Project
- **Repository**: [Bank-Customer-Churn-Intelligence-Risk-Platform](https://github.com/PradeepSargar/Bank-Customer-Churn-Intelligence-Risk-Platform)

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.
