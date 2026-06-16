"""Database loader for Retail Promotion Analytics Platform."""

import os
import pathlib
import sqlite3
import pandas as pd
from dotenv import load_dotenv
import sqlalchemy

def load_environment() -> dict:
    """Loads environment variables for database configuration."""
    load_dotenv()
    config = {
        "use_postgres": os.getenv("USE_POSTGRES", "false").lower() == "true",
        "host": os.getenv("DB_HOST", "localhost"),
        "port": os.getenv("DB_PORT", "5432"),
        "name": os.getenv("DB_NAME", "retail_promotions"),
        "user": os.getenv("DB_USER", "postgres"),
        "password": os.getenv("DB_PASSWORD", "")
    }
    return config

def get_db_connection(config: dict, base_dir: pathlib.Path):
    """Returns database connection/engine based on config."""
    if config["use_postgres"]:
        conn_str = f"postgresql://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['name']}"
        engine = sqlalchemy.create_engine(conn_str)
        print("Connected to PostgreSQL database.")
        return engine
    else:
        db_path = base_dir / "database" / "retail_promotions.db"
        db_path.parent.mkdir(parents=True, exist_ok=True)
        engine = sqlalchemy.create_engine(f"sqlite:///{db_path}")
        print(f"Connected to SQLite database at {db_path}")
        return engine

def generate_dim_date(df_orders: pd.DataFrame) -> pd.DataFrame:
    """Generates the dim_date dimension table from orders timestamps."""
    timestamps = pd.to_datetime(df_orders["order_purchase_timestamp"]).dropna().unique()
    dates = pd.DataFrame({"date_actual": pd.to_datetime(timestamps).date})
    dates = dates.drop_duplicates().sort_values("date_actual").reset_index(drop=True)
    
    dates["date_actual"] = pd.to_datetime(dates["date_actual"])
    dates["date_key"] = dates["date_actual"].dt.strftime("%Y-%m-%d")
    dates["year"] = dates["date_actual"].dt.year
    dates["month"] = dates["date_actual"].dt.month
    dates["day"] = dates["date_actual"].dt.day
    dates["day_of_week"] = dates["date_actual"].dt.dayofweek
    dates["quarter"] = dates["date_actual"].dt.quarter
    
    return dates

def generate_customer_metrics(df_orders: pd.DataFrame) -> pd.DataFrame:
    """Generates the fact_customer_metrics derived table from orders."""
    df_orders["order_purchase_timestamp"] = pd.to_datetime(df_orders["order_purchase_timestamp"])
    max_date = df_orders["order_purchase_timestamp"].max()
    
    metrics = df_orders.groupby("customer_unique_id").agg(
        first_purchase_date=("order_purchase_timestamp", "min"),
        last_purchase_date=("order_purchase_timestamp", "max"),
        total_orders=("order_id", "count"),
        total_revenue=("order_value", "sum"),
        repeat_customer_flag=("repeat_customer_flag", "max")
    ).reset_index()
    
    # Calculate days since last order relative to the max date in the dataset (recency)
    metrics["days_since_last_order"] = (max_date - metrics["last_purchase_date"]).dt.total_seconds() / (24 * 3600)
    metrics.rename(columns={"customer_unique_id": "customer_id"}, inplace=True)
    return metrics

def main() -> None:
    base_dir = pathlib.Path(__file__).resolve().parent.parent
    config = load_environment()
    engine = get_db_connection(config, base_dir)
    
    # Read schema SQL
    schema_path = base_dir / "sql" / "schema.sql"
    with open(schema_path, "r") as f:
        schema_sql = f.read()
        
    # Initialize connection and run schema creation
    with engine.connect() as conn:
        # For sqlite, split commands by semicolon since conn.execute doesn't support multiple commands in a single execute
        if not config["use_postgres"]:
            raw_conn = engine.raw_connection()
            cursor = raw_conn.cursor()
            cursor.executescript(schema_sql)
            raw_conn.commit()
            raw_conn.close()
        else:
            conn.execute(sqlalchemy.text(schema_sql))
            
    print("Database tables initialized successfully.")
    
    # Load processed datasets
    processed_dir = base_dir / "data" / "processed"
    df_orders = pd.read_csv(processed_dir / "processed_orders.csv")
    df_customers = pd.read_csv(processed_dir / "processed_customers.csv")
    df_promotions = pd.read_csv(processed_dir / "promotions.csv")
    
    # Generate dim_date and customer_metrics
    df_dim_date = generate_dim_date(df_orders)
    df_customer_metrics = generate_customer_metrics(df_orders)
    
    # Insert Data into Tables
    # dim_customers
    df_customers.to_sql("dim_customers", con=engine, if_exists="append", index=False, chunksize=1000)
    print("Loaded dim_customers")
    
    # dim_promotions
    df_promotions.to_sql("dim_promotions", con=engine, if_exists="append", index=False)
    print("Loaded dim_promotions")
    
    # dim_date
    df_dim_date.to_sql("dim_date", con=engine, if_exists="append", index=False, chunksize=1000)
    print("Loaded dim_date")
    
    # fact_orders
    # Make sure to format columns to match DB schema
    df_fact_orders = df_orders[[
        "order_id", "customer_unique_id", "order_status", "order_purchase_timestamp",
        "order_value", "promotion_id", "promotion_flag", "days_since_last_order",
        "repeat_customer_flag"
    ]]
    df_fact_orders.to_sql("fact_orders", con=engine, if_exists="append", index=False, chunksize=1000)
    print("Loaded fact_orders")
    
    # fact_customer_metrics
    df_customer_metrics.to_sql("fact_customer_metrics", con=engine, if_exists="append", index=False, chunksize=1000)
    print("Loaded fact_customer_metrics")
    
    print("Database load completed successfully.")

if __name__ == "__main__":
    main()
