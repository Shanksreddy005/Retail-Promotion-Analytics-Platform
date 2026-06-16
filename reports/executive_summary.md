# Executive Summary

## Platform Overview
The **Retail Promotion Analytics Platform** evaluates marketing discount efficacy (P1: 5%, P2: 10%, P3: 20%) against a control group (no discount) using the Olist Brazilian E-Commerce dataset. 

## Strategic Insights
- **Highest Revenue Promotion**: **P1 (5% Discount)** generated the highest total promotional revenue of **$1,862,679.38**, maintaining the highest average order value (AOV) of **$159.97**.
- **Strongest Retention Performance**: **P2 (10% Discount)** achieved the strongest repeat purchase conversion rate of **6.48%**, followed closely by P3 at **6.40%**.
- **Statistical Significance**:
  - **Conversion Rate (Repeat Purchases)**: The conversion rate difference is statistically significant (Z-statistic = `6.7430`, p-value = `0.0000`), showing that promotions correlate with higher repeat purchases.
  - **AOV Impact**: The difference in AOV is not statistically significant (p-value = `0.3440`), indicating that discount incentives did not materially alter the average order size.
- **Recommended Actions**:
  1. **Standardize on P2 (10% Discount)**: P2 yields the highest repeat customer rate while retaining better margins than the 20% discount (P3).
  2. **Transition to Customer-Level Randomization**: To eliminate sample contamination, future experiments must randomize at the customer level rather than the order level.
  3. **Target High-Uplift Regions**: Direct local promotional campaigns to the SP, RJ, and MG regions which account for over 60% of total revenue.
