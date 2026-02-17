# 📦 Supply Chain Demand Forecasting (End-to-End ML Project)

## 🔍 Problem Statement
In supply chain operations, inaccurate demand forecasting leads to **stock-outs**, **overstocking**, and increased holding costs.  
This project builds a **time-aware machine learning system** to forecast **weekly total demand** using historical retail sales data, helping support inventory planning and operational decisions.

---

## 🧠 Why Weekly Aggregate Forecasting?
Instead of forecasting demand per product (which is often sparse and unstable), this project focuses on:

- **Weekly aggregated demand across the supply chain**
- A realistic approach commonly used for **capacity planning, procurement, and logistics**

This design choice ensures:
- Stable learning
- Better generalization
- Easier deployment and interpretation

---

## 📊 Dataset Overview
- **Source:** Public retail demand dataset
- **Target Variable:** `Order_Demand`
- **Key Features:**
  - Date
  - Product, Warehouse, Category (used during aggregation)
- **Time Span:** Multiple years of historical demand

---

## ⚙️ Machine Learning Workflow

### 1️⃣ Data Preprocessing
- Parsed and sorted time-series data
- Handled missing values
- Removed data leakage risks

### 2️⃣ Feature Engineering (Time-Aware)
- **Lag features:** `lag_1`, `lag_2`, `lag_3`
- **Rolling statistics:** `rolling_mean_3`, `rolling_std_3`
- **Calendar features:** `week`, `month`, `year`

---

## 📉 Baseline Model
A naïve baseline was implemented by predicting demand using the **previous week’s demand**.

**Evaluation Metrics:**
- RMSE (Root Mean Squared Error)
- MAPE (Mean Absolute Percentage Error)

This baseline establishes whether machine learning provides real value.

---

## 🤖 Machine Learning Models
- **Linear Regression** (baseline ML model)
- **Random Forest Regressor** (final selected model)

**Why Random Forest?**
- Outperformed baseline and linear regression
- Captures non-linear demand patterns
- Provides built-in feature importance for explainability

---

## 📈 Evaluation Strategy
- **Time-based Train / Validation / Test split**
- No random shuffling (prevents future data leakage)
- Model performance compared against the baseline

---

## 🔍 Model Explainability
Feature importance analysis shows:
- Recent demand history (lag features) is the strongest predictor
- Rolling trends outperform pure calendar features

This makes the model **interpretable and business-friendly**, not a black box.

---

## 🚀 Deployment
- **Backend:** Flask
- **Frontend:** HTML, CSS, JavaScript
- Automatically computes lag & rolling features from historical data

### User Inputs:
- Year
- Month
- Week

### Outputs:
- Predicted weekly demand
- 4-week rolling forecast
- Top influencing features

---

## ⚠️ Limitations
- Forecasts **aggregate supply chain demand**, not per-product demand
- External drivers (promotions, fuel prices) are not fully modeled
- Confidence intervals are not implemented

---

## 🔮 Future Improvements
- Add confidence bands to predictions
- Product or category-level forecasting
- Automated retraining pipeline
- Integration with inventory optimization logic

---

## 🏁 Conclusion
This project demonstrates **real-world machine learning practices**:
- Problem framing
- Time-aware modeling
- Baseline comparison
- Explainability
- Deployment readiness

It reflects how ML systems are designed and deployed in production environments.

---

## 🛠️ Tech Stack
- Python
- Pandas, NumPy
- Scikit-learn
- Matplotlib, Seaborn
- Flask
- HTML, CSS, JavaScript
