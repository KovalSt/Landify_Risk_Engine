# Lendify Risk Strategy Engine: End-to-End Data Analytics Portfolio

**Live Interactive Dashboard:** [Insert Link to your Looker Studio Dashboard here]

## 📌 Executive Summary
Lendify (a simulated fintech company) was experiencing an 8.02% overall default rate on their loan portfolio. I was tasked with identifying the highest-risk borrower segments and building a parameter-driven decision engine to reduce credit loss without unnecessarily sacrificing profitable loan volume. 

By engineering a custom SQL-based credit scorecard, I proved we could reduce the portfolio default rate to **5.48%**, potentially saving the bank over **$150 Million** in expected credit loss. Furthermore, during the data reconciliation phase, I identified a critical logic flaw in the initial risk weighting that prevented the premature deployment of a vulnerable scorecard.

## 🛠️ The Tech Stack
* **Exploratory Data Analysis (EDA):** Python (Pandas, Seaborn)
* **Data Engineering & Modeling:** SQL (Google BigQuery)
* **Business Intelligence & Visualization:** Looker Studio

## 🚀 The Methodology (The "Bridge")

### 1. Identifying the Risk Factors (Python)
I extracted a subset of a 300,000+ row dataset and performed EDA using Pandas to find actionable business arguments:
* **Education Barrier:** Borrowers with only 'Lower Secondary' education defaulted at an 11% rate.
* **The Behavioral Veto:** Borrowers with a history of 'Significant Overdue' debt had a massive 34.6% default rate, overshadowing all other positive traits like high income or academic degrees.

### 2. Building the Decision Engine (SQL / BigQuery)
I translated my Python EDA findings into a production-ready SQL script. 
* I used Common Table Expressions (CTEs) to aggregate massive application and credit bureau tables.
* I engineered a custom `final_credit_score` feature using `CASE WHEN` logic, assigning specific point penalties to high-risk behaviors identified in the EDA phase.

### 3. Executive Dashboard & Data Reconciliation (Looker Studio)
I connected Looker Studio directly to the live BigQuery view using a Custom Query to create a "Decision Engine" for bank executives.
* **The Tool:** An interactive slider allows executives to set a Minimum Credit Score Threshold and instantly see the real-time impact on Total Applications, Default Rates, and Expected Credit Loss.
* **The "Aha!" Moment (Data Reconciliation):** During the UI audit, I discovered a critical flaw in the business logic. Setting a strict threshold of 75 still captured 23,880 projected defaults. The dashboard proved that the initial risk weights (+30 points for a clean record) were too lenient and failed to separate average borrowers from high-risk borrowers. 
* **Business Impact:** Because I caught this in the dashboarding phase via manual SQL reconciliation, I prevented the bank from deploying a flawed risk model, proving the need for a more mathematically rigorous, machine-learning-based scoring system.

## 📈 Key Findings
1. A minimum score threshold of **40** is sufficient to automatically veto 100% of the "Significant Overdue" segment (the most toxic 0.2% of the portfolio).
2. A conservative minimum score threshold of **75** successfully drops the bank's total default rate into the 5% tier, creating a highly secure loan portfolio.
3. **Strategic Pivot:** The standard scorecard method is too generous for the modern credit landscape. The next iteration of this project will involve building a Logistic Regression or XGBoost machine learning model to replace the manual SQL weights.
