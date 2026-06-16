-- Strategic Business Queries for Retail Promotion Analytics Platform

-- 1. Revenue impact and uplift by promotion
-- Estimates the incremental revenue impact compared to the control group
SELECT 
    promotion_id,
    COUNT(order_id) AS total_orders,
    SUM(order_value) AS total_revenue,
    AVG(order_value) AS average_order_value,
    SUM(order_value) - (COUNT(order_id) * (SELECT AVG(order_value) FROM fact_orders WHERE promotion_id = 'CONTROL')) AS estimated_revenue_uplift
FROM fact_orders
GROUP BY promotion_id;

-- 2. Average Order Value (AOV) comparison (Treatment vs Control)
SELECT 
    CASE WHEN promotion_flag = 1 THEN 'Treatment (Promotion)' ELSE 'Control (No Promotion)' END AS group_type,
    COUNT(order_id) AS total_orders,
    SUM(order_value) AS total_revenue,
    AVG(order_value) AS average_order_value
FROM fact_orders
GROUP BY promotion_flag;

-- 3. Customer repeat purchase rates (Retention) by promotion type
SELECT 
    promotion_id,
    COUNT(DISTINCT customer_unique_id) AS total_unique_customers,
    SUM(repeat_customer_flag) AS repeat_customers,
    CAST(SUM(repeat_customer_flag) AS REAL) / COUNT(DISTINCT customer_unique_id) * 100 AS repeat_purchase_rate_pct
FROM fact_orders
GROUP BY promotion_id;

-- 4. Monthly promotion performance trends
SELECT 
    strftime('%Y-%m', order_purchase_timestamp) AS order_month,
    promotion_id,
    COUNT(order_id) AS total_orders,
    SUM(order_value) AS total_revenue,
    AVG(order_value) AS AOV
FROM fact_orders
GROUP BY order_month, promotion_id
ORDER BY order_month ASC, total_revenue DESC;

-- 5. Regional promotion effectiveness by state
SELECT 
    c.customer_state,
    fo.promotion_id,
    COUNT(fo.order_id) AS total_orders,
    SUM(fo.order_value) AS total_revenue,
    AVG(fo.order_value) AS AOV,
    AVG(fo.repeat_customer_flag) * 100 AS repeat_rate_pct
FROM fact_orders fo
JOIN dim_customers c ON fo.customer_unique_id = c.customer_unique_id
GROUP BY c.customer_state, fo.promotion_id
ORDER BY total_revenue DESC;

-- 6. Repeat purchase analysis (Cohort-based summary from customer metrics)
SELECT 
    CASE WHEN total_orders > 1 THEN 'Repeat Buyer' ELSE 'Single Buyer' END AS buyer_segment,
    COUNT(customer_id) AS customer_count,
    SUM(total_revenue) AS total_revenue,
    AVG(total_revenue) AS avg_customer_lifetime_value
FROM fact_customer_metrics
GROUP BY buyer_segment;
