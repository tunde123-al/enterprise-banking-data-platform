"""
Generate accounts linked to customers.
"""
from datetime import datetime
import os

import pandas as pd
import yaml

from .generator_utils import RNG, generate_balance, random_date, set_seed, weighted_choice


def generate_accounts(customers_df: pd.DataFrame, config: dict) -> pd.DataFrame:
    """Generate accounts for the configured customer population."""
    n = config['volumes']['accounts']
    start_date = datetime.strptime(config['date_ranges']['start_date'], "%Y-%m-%d").date()
    end_date = datetime.strptime(config['date_ranges']['end_date'], "%Y-%m-%d").date()
    account_type_weights = config['distributions']['account_type']

    customer_ids = customers_df['customer_id'].tolist()
    accounts = []

    for _ in range(n):
        customer_id = RNG.choice(customer_ids)
        acct_type = weighted_choice(account_type_weights)
        acct_num = f"{RNG.randint(10000000, 99999999)}"
        opened = random_date(start_date, end_date)
        closed = None if RNG.random() < 0.90 else random_date(opened, end_date)
        status = "active" if closed is None else "closed"
        balance = generate_balance(acct_type)
        available = balance * (0.95 + RNG.random()*0.05)

        accounts.append({
            "account_id": len(accounts) + 1,
            "customer_id": customer_id,
            "branch_code": f"BR{RNG.randint(1, 999):03d}",
            "account_number": acct_num,
            "account_type": acct_type,
            "currency": "USD",
            "balance": round(balance, 2),
            "available_balance": round(available, 2),
            "opened_date": opened,
            "closed_date": closed,
            "status": status,
            "created_date": opened,
            "updated_date": opened if RNG.random() < 0.7 else random_date(opened, end_date)
        })

    return pd.DataFrame(accounts)


if __name__ == "__main__":
    customers_df = pd.read_parquet("./data_output/postgres/customers.parquet")
    with open("generator_config.yaml", "r") as f:
        config = yaml.safe_load(f)
    set_seed(config['project']['seed'])
    df = generate_accounts(customers_df, config)
    os.makedirs(config['output']['postgres_dir'], exist_ok=True)
    df.to_parquet(f"{config['output']['postgres_dir']}/accounts.parquet", index=False)
    print(f"Generated {len(df)} accounts.")