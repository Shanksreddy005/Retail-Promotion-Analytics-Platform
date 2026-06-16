-- SQL Views for Retail Promotion Analytics Platform

-- 1. Detailed order overview joining facts and dimensions
CREATE VIEW IF NOT EXISTS v_order_details AS
SELECT 
    fo.order_id,
    fo.customer_unique_id,
    dc.customer_city,
    dc.customer_state,
    fo.order_status,
    fo.order_purchase_timestamp,
    dd.year AS order_year,
    dd.month AS order_month,
    dd.quarter AS order_quarter,
    fo.order_value,
    fo.promotion_id,
    dp.discount_pct,
    fo.promotion_flag,
    fo.days_since_last_order,
    fo.repeat_customer_flag
FROM fact_orders fo
LEFT JOIN dim_customers dc ON fo.customer_unique_id = dc.customer_unique_id
LEFT JOIN dim_promotions dp ON fo.promotion_id = dp.promotion_id
LEFT JOIN dim_date dd ON strftime('%Y-%m-%d', fo.order_purchase_timestamp) = dd.date_key;

-- 2. Promotion summary performance view
CREATE VIEW IF NOT EXISTS v_promotion_performance AS
SELECT 
    promotion_id,
    COUNT(order_id) AS total_orders,
    SUM(order_value) AS total_revenue,
    AVG(order_value) AS average_order_value,
    SUM(promotion_flag) AS total_promo_orders,
    AVG(repeat_customer_flag) * 100 AS repeat_customer_percentage
FROM fact_orders
GROUP BY promotion_id;
