"""Promotion simulation generator for Retail Promotion Analytics Platform."""

import pathlib
import pandas as pd
import numpy as np

def main() -> None:
    # Set paths using pathlib
    base_dir = pathlib.Path(__file__).resolve().parent.parent
    raw_dir = base_dir / "data" / "raw"
    processed_dir = base_dir / "data" / "processed"
    
    # Ensure directories exist
    raw_dir.mkdir(parents=True, exist_ok=True)
    processed_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Create promotions.csv
    promotions_data = {
        "promotion_id": ["P1", "P2", "P3"],
        "discount_pct": [5, 10, 20]
    }
    df_promotions = pd.DataFrame(promotions_data)
    df_promotions.to_csv(processed_dir / "promotions.csv", index=False)
    print("Created promotions.csv in data/processed/")

    # 2. Assign promotions randomly to 35% of orders
    orders_path = base_dir / "olist_orders_dataset.csv"
    if not orders_path.exists():
        orders_path = raw_dir / "olist_orders_dataset.csv"
        
    if not orders_path.exists():
        raise FileNotFoundError(f"Could not find olist_orders_dataset.csv in {base_dir} or {raw_dir}")
        
    df_orders = pd.read_csv(orders_path)
    order_ids = df_orders["order_id"].unique()
    
    # Fixed random seed for reproducibility
    np.random.seed(42)
    
    # Shuffle and select 35% for promotions
    n_orders = len(order_ids)
    n_promo = int(n_orders * 0.35)
    
    shuffled_indices = np.random.permutation(n_orders)
    promo_indices = shuffled_indices[:n_promo]
    
    # Map promotion IDs to the selected promo orders
    promo_choices = np.random.choice(["P1", "P2", "P3"], size=n_promo)
    
    order_promo_map = {order_id: "CONTROL" for order_id in order_ids}
    for idx, promo_id in zip(promo_indices, promo_choices):
        order_promo_map[order_ids[idx]] = promo_id
        
    df_order_promo = pd.DataFrame(
        list(order_promo_map.items()), 
        columns=["order_id", "promotion_id"]
    )
    
    df_order_promo.to_csv(processed_dir / "order_promotions.csv", index=False)
    print("Created order_promotions.csv in data/processed/")

if __name__ == "__main__":
    main()
