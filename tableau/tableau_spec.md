# Tableau Dashboard Specification

## Pages
1. **Executive Overview Dashboard**: High-level sales performance and campaign metrics.
2. **Promotion Detail Analysis**: Breakdowns of discount efficiency, uplift, and regional response.
3. **Retention & Cohort Behavior**: Long-term repeat purchaser trends.

## KPIs
- **Total Revenue (Gross Sales)**: `SUM([order_value])`
- **Total Orders**: `COUNTD([order_id])`
- **AOV (Average Order Value)**: `SUM([order_value]) / COUNTD([order_id])`
- **Overall Repeat Customer Rate**: `SUM([repeat_customer_flag]) / COUNTD([customer_unique_id])`
- **Estimated Campaign Uplift**: Difference between promotion average order value vs control.

## Charts
- **Sales Trends Line Chart**: Monthly revenue partitioned by `promotion_flag` or `promotion_id`.
- **Promotion AOV vs. Control Boxplot**: Visualization of distribution shift by campaign type.
- **Regional Heat Map**: Map of Brazil colored by `AOV Uplift %` or total revenue from promotions.
- **Cohort Retention Matrix**: Cohort Month on rows, Cohort Index (0-12 months) on columns, colored by `Retention Rate %`.

## Filters
- **Order Date / Year / Quarter**: Interactive date range slider.
- **Promotion ID / Type**: Dropdown (All, CONTROL, P1, P2, P3).
- **Customer State / City**: Multiselect list.

## Calculated Fields
- **Promotion Group**:
  ```sql
  IF [promotion_flag] = 1 THEN "Promotion Group" ELSE "Control Group" END
  ```
- **AOV Calculation**:
  ```sql
  SUM([order_value]) / COUNTD([order_id])
  ```
- **Repeat Conversion %**:
  ```sql
  (SUM([repeat_customer_flag]) / COUNTD([customer_unique_id])) * 100
  ```
