# 🏦 Bank Customer Churn Intelligence & Risk Platform

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Scikit-Learn](https://img.shields.io/badge/scikit_learn-1.3+-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![SHAP](https://img.shields.io/badge/SHAP-Explainable_AI-7C3AED?style=for-the-badge)](https://shap.readthedocs.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

An enterprise-grade **Bank Customer Churn Prediction and Risk Intelligence Platform** built with Python, Gradient Boosting, 5-Fold Stratified Cross-Validation, Decision Policy Optimization, Value-at-Risk Prioritization, SHAP Explainable AI (XAI), and a modern glassmorphic Streamlit analytics dashboard.

---

## 🎯 Executive Overview

Customer acquisition in retail banking costs **5× to 25× more** than retaining existing high-value depositors. This system empowers branch managers, retention teams, and executive leadership to:
1. **Identify At-Risk Accounts in Real-Time** with calibrated probability scores (0%–100%) and a standardized 3-tier risk classification (*Low <30%, Medium 30%–70%, High ≥70%*).
2. **Evaluate Model Stability via 5-Fold Stratified Cross-Validation** to ensure generalizability and prevent data leakage before holdout test evaluation.
3. **Optimize Decision Boundaries** using empirical threshold trade-off analysis (Default $0.50$ high precision vs Recommended $0.35$ high recall retention campaign).
4. **Prioritize Accounts by Value-at-Risk (VAR)** to shift from simple probability ranking to revenue-maximizing business prioritization.
5. **Audit Model Decisions** using game-theoretic SHAP TreeExplainer attribution (Global feature rankings, Dependence plots, and Local Waterfall diagrams).
6. **Simulate Predictive Retention Levers** (membership status, product holdings, balance incentives) in an interactive what-if sandbox.
7. **Process Batch Customer Records** via CSV uploads for automated daily risk scoring and CRM pipeline integration.

---

## 🏆 Model Evaluation & Validation Benchmarks

Five classification architectures were trained on 8,000 training records using **5-Fold Stratified Cross-Validation** and evaluated against an untouched 2,000-record holdout test cohort. The **Gradient Boosting Classifier** emerged as the undisputed production champion:

### 1. 5-Fold Stratified Cross-Validation Benchmark (8,000 Records)
| Model | Mean Accuracy $\pm$ Std | Mean Precision $\pm$ Std | Mean Recall $\pm$ Std | Mean F1-Score $\pm$ Std | Mean ROC-AUC $\pm$ Std |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **🏆 Gradient Boosting** | **86.31% ± 0.99%** | **77.22% ± 3.17%** | **46.44% ± 3.56%** | **57.98% ± 3.65%** | **86.48% ± 0.95%** |
| **⚡ XGBoost** | 86.08% ± 0.79% | 75.55% ± 2.71% | 46.75% ± 2.55% | 57.75% ± 2.71% | 86.47% ± 0.96% |
| **🌲 Random Forest** | 85.82% ± 0.84% | 74.60% ± 2.81% | 46.07% ± 2.75% | 56.96% ± 2.90% | 85.02% ± 1.22% |
| **📈 Logistic Regression** | 81.05% ± 0.67% | 59.67% ± 4.43% | 21.41% ± 2.58% | 31.48% ± 3.27% | 76.28% ± 1.93% |
| **🌿 Decision Tree** | 78.69% ± 0.63% | 47.81% ± 1.44% | 50.18% ± 3.64% | 48.91% ± 2.15% | 68.08% ± 1.54% |

### 2. Final Holdout Test Benchmark (2,000 Untouched Records)
| Model | Test Accuracy | Test Precision | Test Recall | Test F1-Score | Test ROC-AUC | Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **🏆 Gradient Boosting** | **87.00%** | **79.28%** | **48.89%** | **60.49%** | **87.08%** | **Production Champion** |
| **⚡ XGBoost** | 86.65% | 77.34% | 48.65% | 59.73% | 86.72% | Alternative Candidate |
| **🌲 Random Forest** | 86.40% | 75.76% | 49.14% | 59.61% | 86.24% | Benchmark |
| **📈 Logistic Regression** | 80.80% | 58.91% | 18.67% | 28.36% | 77.48% | Baseline |
| **🌿 Decision Tree** | 78.60% | 47.72% | 51.60% | 49.59% | 68.85% | Exploratory |

---

## 🎚️ Decision Threshold Optimization (via 5-Fold OOF Cross-Validation)

Decision-threshold selection is performed strictly using **Out-Of-Fold (OOF) predictions** generated from 5-fold stratified cross-validation on the 8,000-record training set. The 20% holdout test set (2,000 records) remains untouched until final unbiased evaluation.

### Out-Of-Fold (OOF) Training Calibration (8,000 Records)
| Threshold ($T$) | OOF Accuracy | OOF Precision | OOF Recall | OOF F1-Score | OOF Churners Captured (TP) | Operating Policy Context |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **0.20** | 80.10% | 50.80% | **74.11%** | 60.28% | 1,208 / 1,630 | ⚡ Early Warning Automated Nudges |
| **0.30** | 84.64% | 62.01% | 63.50% | **62.75%** | 1,035 / 1,630 | 🔄 High-Coverage Campaign |
| **0.35** | **85.51%** | **66.23%** | **58.96%** | **62.38%** | **961 / 1,630** | **⭐ Selected OOF Policy (Optimal Balance)** |
| **0.50** | **86.31%** | **77.32%** | **46.44%** | **58.03%** | **757 / 1,630** | **🎯 Default Precision Mode** |

### Unbiased Holdout Test Verification (2,000 Records)
- **Default 0.50 Mode**: Accuracy $87.00\%$, Precision $79.28\%$, Recall $48.89\%$, F1 $60.49\%$, ROC-AUC $87.08\%$ (199 / 407 churners caught).
- **Selected 0.35 Policy**: Accuracy $85.75\%$, Precision $66.67\%$, Recall $59.95\%$, F1 $63.13\%$ (244 / 407 churners caught, **+45 extra churners**, $+22.61\%$ relative gain).
- *Illustrative Retention Simulation*: In a scenario model assuming average $\text{CLV} = \$2,500$, save rate $= 25\%$, and contact cost $= \$50$, adopting the $0.35$ policy protects an estimated **+$22,375 in net added value** over baseline.

---

## 💼 Business Prioritization & Expected Loss Exposure Heuristic

To bridge the gap between churn likelihood and commercial exposure:
- **Customer Value Proxy (CVP)**: $\text{CVP} = \text{Balance} + (0.5 \times \text{EstimatedSalary})$ *(Operational heuristic combining liquid deposits and annual earnings capacity)*
- **Expected Loss Exposure Index**: $\text{Loss Exposure} = \text{CVP} \times \text{Predicted Churn Probability}$

### 4-Tier Strategic Retention Matrix:
1. 🔴 **Critical Priority**: Churn Probability $\ge 70\%$ **AND** High Value (Top 30% CVP) &rarr; *24-Hour RM Escalation & Custom Fee Waiver*.
2. 🟠 **High Priority**: Churn Probability $\ge 70\%$ **OR** (Medium Churn $30\%–70\%$ with High Value) &rarr; *48-Hour Retention Call & Competitive Rate Lock*.
3. 🟡 **Medium Priority**: Medium Churn ($30\%–70\%$) with Low/Med Value &rarr; *7-Day Automated Digital Nudge*.
4. 🟢 **Low Priority / Nurture**: Low Churn ($< 30\%$) &rarr; *Standard Relationship Maintenance & Cross-Sell*.

*Governance Note*: Standardized risk tiers ($<30\%$ Low, $30\%-70\%$ Medium, $\ge 70\%$ High) remain completely independent of the operating classification decision threshold. Business prioritization is an operational decision heuristic rather than formal regulatory Basel Value-at-Risk.

---

## 🏗️ System Architecture & Directory Layout

```
Bank Customer Churn Intelligence & Risk Platform/
│
├── .streamlit/
│   └── config.toml                 # Streamlit UI & server configuration
│
├── data/
│   ├── Processed/
│   │   └── customer_risk_report.csv # Cleaned & engineered European bank cohort (10K rows)
│   └── Raw/
│       └── European_Bank.csv        # Original raw banking dataset
│
├── models/
│   ├── gradient_boosting_model.pkl  # Trained production Gradient Boosting classifier
│   ├── scaler.pkl                  # Fitted StandardScaler object
│   ├── label_encoder.pkl           # Categorical encoder mappings
│   ├── shap_explainer.pkl          # SHAP TreeExplainer object
│   ├── shap_values.pkl             # Precomputed SHAP matrix (2,000 hold-out records)
│   ├── feature_importance.pkl      # Feature importance rankings
│   ├── feature_names.pkl           # Feature name registry
│   └── X_test.pkl                  # Hold-out test dataset
│
├── notebooks/
│   └── Bank_Churn_Analysis.ipynb   # 26-Section end-to-end analytical & ML research notebook
│
├── dashboard/                      # Multi-Page Streamlit Enterprise Application
│   ├── app.py                      # Central Command Hub & Real-time Risk Scorer
│   ├── pages/
│   │   ├── 01_Executive_Overview.py    # Portfolio health, KPIs, and executive strategy
│   │   ├── 02_Customer_Analytics.py    # 15+ Exploratory analytics & demographic modules
│   │   ├── 03_Risk_Portfolio.py        # Customer triage engine with Value-at-Risk ranking
│   │   ├── 04_Model_Performance.py     # Holdout test & 5-Fold CV benchmarks
│   │   ├── 05_Model_Explainability.py  # XAI Suite (SHAP beeswarm, dependence, waterfall)
│   │   ├── 06_Customer_Risk_Scoring.py # Single & Batch scoring with threshold policy selector
│   │   ├── 07_Scenario_Simulator.py    # Predictive what-if sandbox with delta tracking
│   │   └── 08_Platform_Overview.py     # System architecture, stack & methodology specs
│   │
│   ├── components/                 # Reusable Glassmorphic UI Components
│   ├── services/                   # Business Logic & Caching Layer
│   └── utils/                      # Styling, Formatters & Constants
│
├── requirements.txt                # Python package dependencies
└── README.md                       # Master project documentation
```

---

## ⚡ Getting Started

### 1. Set Up Environment

```bash
# Clone the repository
git clone https://github.com/pradeepsargar/bank-churn-intelligence.git
cd "Bank Customer Churn Intelligence & Risk Platform"

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\activate
```

### 2. Install Dependencies & Run

```bash
pip install -r requirements.txt
streamlit run dashboard/app.py
```

The application will launch in your browser at `http://localhost:8501`.

---

## 🧠 Explainable AI (XAI) Integration

The platform uses **SHAP (SHapley Additive exPlanations)** to ensure full regulatory compliance and transparent decision audits:
- **Global Feature Drivers**: Age, Number of Products, Inactive Membership, and Geography (Germany) emerge as the primary predictive indicators.
- **Local Waterfall Attributions**: Step-by-step feature breakdown for any individual customer explaining how their probability score was derived from the base cohort rate.
- **Methodological Boundary**: Predictive associations from the model reflect statistical patterns in historical data rather than guaranteed causal outcomes.

---

## 👨‍💻 Author & Project Credits

- **Developer**: Pradeep Sargar
- **Institution**: University of Mumbai
- **Discipline**: Computer Engineering
- **Focus**: Applied Machine Learning, Risk Intelligence, Fintech Decision Platforms
- **Project**: Unified Mentor Advanced Analytics Project

---

## 📄 License

This project is licensed under the MIT License — see the LICENSE file for details.
