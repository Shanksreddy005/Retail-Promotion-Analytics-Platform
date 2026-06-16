# Excel Dashboard Specification

## Pivot Tables
1. **Revenue by Promotion Group**:
   - Rows: `promotion_id`
   - Values: Sum of `order_value` (Formatted as Currency), Count of `order_id` (Formatted as Integer), Average of `order_value` (Formatted as Currency).
2. **Monthly Orders Trend**:
   - Rows: `order_purchase_timestamp` (grouped by Month/Year)
   - Columns: `promotion_flag` (0, 1)
   - Values: Count of `order_id`.
3. **Repeat Purchase rate by state**:
   - Rows: `customer_state`
   - Values: Average of `repeat_customer_flag` (Formatted as Percentage).

## Slicers
- `promotion_id`
- `customer_state`
- `order_purchase_timestamp` (Timeline filter or Slicer by Year)

## Conditional Formatting
- **AOV Cells**: Color scale (Green to Red) to highlight high-value order averages.
- **Repeat Purchase %**: Data bars (Blue) on the customer metrics summary.
- **Sales Uplift**: Highlight cells > $0 in soft green and < $0 in soft red.

## Recommended Layout
- **Sheet 1 (`Summary Dashboard`)**:
  - Top Row: 4 KPI Cards (Total Sales, Total Orders, Overall AOV, Overall Repeat %).
  - Left Column: Slicers (`promotion_id`, `customer_state`).
  - Main Body: Sales Line Chart (Monthly Trends) and Bar Chart (AOV by Promotion).
- **Sheet 2 (`Pivot Calculations`)**:
  - Raw Pivot tables acting as the backend data source for dashboard widgets.
- **Sheet 3 (`Processed Data`)**:
  - Raw data dump of `processed_orders.csv` or imported via Power Query.
