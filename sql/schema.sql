-- DDL for Retail Promotion Analytics Platform

-- Dimension: Customers
CREATE TABLE IF NOT EXISTS dim_customers (
    customer_unique_id VARCHAR(50) PRIMARY KEY,
    customer_city VARCHAR(100),
    customer_state VARCHAR(10)
);

-- Dimension: Promotions
CREATE TABLE IF NOT EXISTS dim_promotions (
    promotion_id VARCHAR(20) PRIMARY KEY,
    discount_pct INT
);

-- Dimension: Date
CREATE TABLE IF NOT EXISTS dim_date (
    date_key VARCHAR(10) PRIMARY KEY,
    date_actual DATE,
    year INT,
    month INT,
    day INT,
    day_of_week INT,
    quarter INT
);

-- Fact: Orders
CREATE TABLE IF NOT EXISTS fact_orders (
    order_id VARCHAR(50) PRIMARY KEY,
    customer_unique_id VARCHAR(50),
    order_status VARCHAR(20),
    order_purchase_timestamp TIMESTAMP,
    order_value NUMERIC(10, 2),
    promotion_id VARCHAR(20),
    promotion_flag INT,
    days_since_last_order NUMERIC(10, 2),
    repeat_customer_flag INT,
    FOREIGN KEY (customer_unique_id) REFERENCES dim_customers(customer_unique_id),
    FOREIGN KEY (promotion_id) REFERENCES dim_promotions(promotion_id)
);

-- Fact: Customer Metrics (derived table)
CREATE TABLE IF NOT EXISTS fact_customer_metrics (
    customer_id VARCHAR(50) PRIMARY KEY,
    first_purchase_date TIMESTAMP,
    last_purchase_date TIMESTAMP,
    total_orders INT,
    total_revenue NUMERIC(12, 2),
    repeat_customer_flag INT,
    days_since_last_order NUMERIC(10, 2),
    FOREIGN KEY (customer_id) REFERENCES dim_customers(customer_unique_id)
);
