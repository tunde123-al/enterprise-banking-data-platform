"""Generate transaction records."""
import os
from datetime import datetime

import pandas as pd
import yaml

from .generator_utils import RNG, generate_transaction_amount, random_timestamp, set_seed, weighted_choice


def generate_transactions(accounts_df: pd.DataFrame, merchants_df: pd.DataFrame, config: dict) -> pd.DataFrame:
    """Generate transactions with realistic patterns."""
    n = config['volumes']['transactions']
    start_date = datetime.strptime(config['date_ranges']['start_date'], "%Y-%m-%d").date()
    end_date = datetime.strptime(config['date_ranges']['end_date'], "%Y-%m-%d").date()
    txn_type_weights = config['distributions']['transaction_type']
    txn_cat_weights = config['distributions']['transaction_category']

    account_ids = accounts_df['account_id'].tolist()
    account_dict = accounts_df.set_index('account_id').to_dict(orient='index')
    merchant_ids = merchants_df['merchant_id'].tolist() if not merchants_df.empty else [1]

    transactions = []
    balances = {acc_id: account_dict[acc_id]['balance'] for acc_id in account_ids}

    for i in range(n):
        acc_id = RNG.choice(account_ids)
        txn_type = weighted_choice(txn_type_weights)
        txn_date = random_timestamp(start_date, end_date)
        amount = round(max(1.0, min(generate_transaction_amount(txn_type), 50000)), 2)

        if txn_type in ['deposit']:
            sign = 1
        elif txn_type in ['withdrawal', 'payment', 'fee']:
            sign = -1
        else:
            sign = 1 if RNG.random() < 0.5 else -1

        new_balance = balances[acc_id] + (sign * amount)
        if new_balance < -1000:
            if balances[acc_id] <= -1000:
                amount = round(max(5.0, min(generate_transaction_amount('deposit'), 5000)), 2)
                sign = 1
                new_balance = balances[acc_id] + amount
                txn_type = 'deposit'
            else:
                amount = round(max(1.0, abs(balances[acc_id] + 1000)), 2)
                new_balance = -1000
        balances[acc_id] = new_balance

        merchant_id = RNG.choice(merchant_ids) if txn_type in ['payment', 'withdrawal'] else None
        if txn_type == 'deposit':
            merchant_id = None
            cat = "income"
        else:
            cat = weighted_choice(txn_cat_weights)

        transactions.append({
            "transaction_id": i + 1,
            "account_id": acc_id,
            "merchant_id": merchant_id,
            "transaction_reference": f"TXN{RNG.randint(1000000,9999999):07d}",
            "amount": amount,
            "currency": "USD",
            "transaction_type": txn_type,
            "transaction_category": cat,
            "transaction_date": txn_date,
            "balance_after": round(new_balance, 2),
            "status": "completed" if RNG.random() < 0.98 else "declined",
            "description": f"{txn_type} at {RNG.choice(['Store', 'Online', 'ATM', 'Branch'])}",
            "fee": round(RNG.uniform(0, 5), 2) if txn_type != 'deposit' else 0,
            "tax": 0
        })

    df = pd.DataFrame(transactions)
    # Nullable integer keeps merchant_id as 225 (not 225.0) alongside missing values.
    df["merchant_id"] = df["merchant_id"].astype("Int64")
    return df


if __name__ == "__main__":
    accounts_df = pd.read_parquet("./data_output/postgres/accounts.parquet")
    merchants_df = pd.read_parquet("./data_output/postgres/merchants.parquet")
    with open("generator_config.yaml", "r") as f:
        config = yaml.safe_load(f)
    set_seed(config['project']['seed'])
    df = generate_transactions(accounts_df, merchants_df, config)
    os.makedirs(config['output']['postgres_dir'], exist_ok=True)
    df.to_parquet(f"{config['output']['postgres_dir']}/transactions.parquet", index=False)
    print(f"Generated {len(df)} transactions.")