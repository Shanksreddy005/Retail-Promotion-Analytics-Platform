# Detailed Findings Report

## Methodology
- **Treated Population Assignment**: Promotions were assigned randomly to exactly 35.00% of orders using a fixed random seed of `42` in `scripts/generate_promotions.py`. The remaining 65.00% of orders serve as the control group.
- **Analysis Execution**: Processed records are stored in a SQLite database and queried using business queries. A/B testing is performed using a two-proportion Z-test for customer-level conversion rates and independent t-tests for continuous value metrics.

## Statistical Assumptions & Significance
- **Significance Level**: \(\alpha = 0.05\)
- **Hypotheses for Conversion Rate**:
  - \(H_0\): \(P_{promo} = P_{control}\) (Promotions do not increase repeat purchase conversion)
  - \(H_1\): \(P_{promo} > P_{control}\) (Promotions increase repeat purchase conversion)
- **Observations & Calculations**:
  - Conversion Z-statistic: `6.7430`
  - Z-test P-value: `0.0000` (Highly statistically significant; reject \(H_0\))
  - Treatment Conversion 95% Confidence Interval: `4.89%` to `5.35%`
  - Control Conversion 95% Confidence Interval: `4.03%` to `4.34%`
  - AOV T-test statistic: `-0.9463`, P-value: `0.3440` (Not statistically significant; fail to reject \(H_0\) for AOV)

## Baseline Comparability & Imbalances
Because the simulation randomized assignments at the *order* level rather than the *customer* level:
1. **User Overlap**: Customers with multiple purchases may have had one purchase in the Control group and another in the Treatment group. This cross-contamination explains why the customer counts in the summary table sum to more than the total unique customers.
2. **AOV Balance**: AOV is balanced between treatment ($158.44) and control ($159.80), indicating no material baseline difference.
3. **Geographic Distribution**: Order assignments are balanced proportionally across states, matching the overall Olist distribution (SP represents ~42% of both cohorts).

## Final Performance Summary Table
| Group | Customers (Unique) | Orders | Revenue ($) | AOV ($) | Repeat Purchase Rate (%) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **CONTROL** | 63,148 | 64,637 | 10,329,292.21 | 159.80 | 6.39% |
| **P1 (5%)** | 11,594 | 11,644 | 1,862,679.38 | 159.97 | 6.18% |
| **P2 (10%)**| 11,516 | 11,569 | 1,841,087.06 | 159.14 | 6.48% |
| **P3 (20%)**| 11,532 | 11,591 | 1,810,494.59 | 156.20 | 6.40% |

## Limitations & Risks
- **Synthetic Assignment**: Promotions were synthetically assigned post-hoc rather than originating from observed business interventions. The findings demonstrate a rigorous experimentation framework rather than causal proof of historical promotion effectiveness.
- **Sample Contamination**: Order-level randomization leads to user-level cross-contamination, which violates the independence assumption of the Z-test for customer-level conversion.
- **Seasonality & Product Mix**: The analysis does not account for seasonality shifts or category-specific demand which can confound promotional responsiveness.
