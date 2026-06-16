"""ETL pipeline for Retail Promotion Analytics Platform."""

import shutil
import pathlib
import pandas as pd
import numpy as np

def check_missing_and_duplicates(df: pd.DataFrame, name: str) -> pd.DataFrame:
    """Checks missing values, logs them, and removes duplicates."""
    missing_count = df.isnull().sum().sum()
    dup_count = df.duplicated().sum()
    print(f"[{name}] Missing values: {missing_count}, Duplicate rows: {dup_count}")
    if dup_count > 0:
        df = df.drop_duplicates()
        print(f"[{name}] Removed duplicate rows.")
    return df

def main() -> None:
    # Set up directory paths
    base_dir = pathlib.Path(__file__).resolve().parent.parent
    raw_dir = base_dir / "data" / "raw"
    processed_dir = base_dir / "data" / "processed"
    
    raw_dir.mkdir(parents=True, exist_ok=True)
    processed_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Copy original Olist CSVs from root to data/raw to preserve data lineage
    csv_files = [
        "olist_customers_dataset.csv",
        "olist_geolocation_dataset.csv",
        "olist_order_items_dataset.csv",
        "olist_order_payments_dataset.csv",
        "olist_order_reviews_dataset.csv",
        "olist_orders_dataset.csv",
        "olist_products_dataset.csv",
        "olist_sellers_dataset.csv",
        "product_category_name_translation.csv"
    ]
    
    for filename in csv_files:
        src = base_dir / filename
        dest = raw_dir / filename
        if src.exists() and not dest.exists():
            shutil.copy2(src, dest)
            print(f"Copied {filename} to data/raw/")
            
    # 2. Extract Data
    df_orders = pd.read_csv(raw_dir / "olist_orders_dataset.csv")
    df_order_items = pd.read_csv(raw_dir / "olist_order_items_dataset.csv")
    df_customers = pd.read_csv(raw_dir / "olist_customers_dataset.csv")
    
    order_promotions_path = processed_dir / "order_promotions.csv"
    if not order_promotions_path.exists():
        raise FileNotFoundError("Run generate_promotions.py first to create order_promotions.csv.")
    df_order_promotions = pd.read_csv(order_promotions_path)
    
    # 3. Clean Data
    df_orders = check_missing_and_duplicates(df_orders, "Orders")
    df_order_items = check_missing_and_duplicates(df_order_items, "Order Items")
    df_customers = check_missing_and_duplicates(df_customers, "Customers")
    
    # 4. Feature Engineering
    # Calculate order_value (price + freight) per order
    df_item_totals = df_order_items.groupby("order_id").agg(
        order_value=("price", "sum"),
        freight_value=("freight_value", "sum")
    ).reset_index()
    # Add freight to order value to get total cost paid by customer
    df_item_totals["order_value"] = df_item_totals["order_value"] + df_item_totals["freight_value"]
    
    # Merge orders with customer unique_ids
    df_orders_merged = df_orders.merge(df_customers, on="customer_id", how="inner")
    
    # Merge order value
    df_orders_merged = df_orders_merged.merge(df_item_totals, on="order_id", how="left")
    df_orders_merged["order_value"] = df_orders_merged["order_value"].fillna(0.0)
    
    # Merge promotions
    df_orders_merged = df_orders_merged.merge(df_order_promotions, on="order_id", how="left")
    df_orders_merged["promotion_id"] = df_orders_merged["promotion_id"].fillna("CONTROL")
    df_orders_merged["promotion_flag"] = df_orders_merged["promotion_id"].apply(
        lambda x: 0 if x == "CONTROL" else 1
    )
    
    # Sort by customer and purchase timestamp to compute days_since_last_order
    df_orders_merged["order_purchase_timestamp"] = pd.to_datetime(df_orders_merged["order_purchase_timestamp"])
    df_orders_merged = df_orders_merged.sort_values(by=["customer_unique_id", "order_purchase_timestamp"])
    
    df_orders_merged["prev_purchase_timestamp"] = df_orders_merged.groupby("customer_unique_id")["order_purchase_timestamp"].shift(1)
    df_orders_merged["days_since_last_order"] = (
        df_orders_merged["order_purchase_timestamp"] - df_orders_merged["prev_purchase_timestamp"]
    ).dt.total_seconds() / (24 * 3600)
    df_orders_merged["days_since_last_order"] = df_orders_merged["days_since_last_order"].fillna(-1)
    
    # Calculate repeat customer flag
    customer_order_counts = df_orders_merged.groupby("customer_unique_id")["order_id"].transform("count")
    df_orders_merged["repeat_customer_flag"] = (customer_order_counts > 1).astype(int)
    
    # Clean up and select columns for final processed orders
    processed_orders = df_orders_merged[[
        "order_id", "customer_id", "customer_unique_id", "order_status",
        "order_purchase_timestamp", "order_value", "promotion_id",
        "promotion_flag", "days_since_last_order", "repeat_customer_flag",
        "customer_city", "customer_state"
    ]]
    
    # Save processed files
    processed_orders.to_csv(processed_dir / "processed_orders.csv", index=False)
    
    # Clean and save customer demographics
    processed_customers = df_customers.drop_duplicates(subset=["customer_unique_id"])[[
        "customer_unique_id", "customer_city", "customer_state"
    ]]
    processed_customers.to_csv(processed_dir / "processed_customers.csv", index=False)
    
    # Copy category translation to processed
    shutil.copy2(
        raw_dir / "product_category_name_translation.csv", 
        processed_dir / "product_category_name_translation.csv"
    )
    
    print("ETL complete. Processed files written to data/processed/")

if __name__ == "__main__":
    main()
