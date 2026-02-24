# Stock Market Risk Analysis  
### Credit Risk Evaluation using Altman Z-Score and Merton Structural Model

**Author:** José Armando Melchor Soto  
**Course:** Credit Models  
**Institution:** ITESO  

---

##  Project Description

This project evaluates the **credit risk and insolvency probability** of publicly traded companies using two classical financial risk models:

- **Altman Z-Score**
- **Merton Structural Default Model**

The objective is to determine whether a company should be **approved or denied for credit**, based on quantitative financial indicators obtained from real market data.

The analysis automatically downloads financial statements and market information from the internet using company ticker symbols and performs a fully automated risk assessment.

---

##  Models Implemented

---

###  Altman Z-Score Model

The Altman Z-Score predicts the probability that a company will enter bankruptcy within approximately two years by combining five accounting-based financial ratios measuring:

- Liquidity  
- Profitability  
- Operating efficiency  
- Leverage  
- Asset turnover  

The implemented formula corresponds to the **public manufacturing firms version**:

$$
Z = 1.2X_1 + 1.4X_2 + 3.3X_3 + 0.6X_4 + 1.0X_5
$$

Where:

- $X_1$$ = Working Capital / Total Assets  
- $X_2$$ = Retained Earnings / Total Assets  
- $X_3$$ = EBIT / Total Assets  
- $X_4$$ = Market Value of Equity / Total Liabilities  
- $X_5$$ = Sales / Total Assets  

### Interpretation

| Z-Score | Risk Level | Interpretation |
|---|---|---|
| Z < 1.8 | Unsafe | High bankruptcy risk |
| 1.8 ≤ Z ≤ 3 | Grey Zone | Moderate risk |
| Z > 3 | Safe | Low bankruptcy risk |

Companies below **1.8** present significant financial distress, while firms above **3** are considered financially stable. :contentReference[oaicite:0]{index=0}

---

### ✅ Merton Model (Structural Credit Risk Model)

The Merton Model views a company's equity as a call option on its assets, where default occurs if asset value falls below debt obligations at maturity.

Key variables:

- $V$: Firm value (Equity + Debt)
- $D$: Debt level (default point)
- $σ$: Asset volatility
- $r$: Risk-free rate
- $T$: Time horizon

---

#### Distance to Default

$$
DD = \frac{\ln(V/D) + (r + \sigma^2/2)T}{\sigma \sqrt{T}}
$$

A lower Distance to Default implies higher insolvency risk.

---

#### Probability of Default

$$ PD = 1 - N(DD)$$

Where $N(\cdot)$ is the cumulative standard normal distribution.

---

##  Credit Decision Rule

A unified decision rule combines both models:

| Condition | Decision |
|---|---|
| Z > 3 and PD < 5% | ✅ APPROVE |
| Z < 1.8 or PD > 20% | ❌ DENY |
| Otherwise | ⚠ REVIEW |

This rule is implemented in the base `RiskModel` class and automatically applied to all companies.

---

## Automatic Financial Data Download

The system downloads:

- Balance sheets
- Income statements
- Market capitalization
- Historical stock prices

using **Yahoo Finance API**, allowing analysis of **any ticker symbol**.

Example:

`AZO, MA, BA, F` 



---

## Interactive Dashboard

The Streamlit dashboard provides:

- Altman Z-Score visualization  
- Distance to Default analysis  
- Probability of Default comparison  
- Automated Credit Decision Table  

### Run locally:

```bash
streamlit run main.py
```

## Installation

### Clone repository:

git clone https://github.com/ppmelch/Stock_Market_Risk_Analysis.git
cd Stock_Market_Risk_Analysis

### Install dependencies:

pip install -r requirements.txt