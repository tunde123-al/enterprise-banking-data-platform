"""Generate high-volume banking event rows for Cassandra (partitioned parquet)."""
import os
import random
import uuid
from datetime import date, timedelta

import pandas as pd

from .generator_utils import RNG, random_timestamp


def _deterministic_event_id(transaction_id, index):
    """Stable UUID so a re-run with the same seed produces identical rows."""
    return uuid.uuid5(uuid.NAMESPACE_DNS, f"{transaction_id}:{index}")


def generate_cassandra_events(transactions_df, config, output_dir=None):
    n = config['volumes']['cassandra_events']
    txn_ids = transactions_df['transaction_id'].sample(n, replace=True).tolist()
    events = []
    unique_accounts = transactions_df['account_id'].unique()

    for idx, txn_id in enumerate(txn_ids):
        account_id = RNG.choice(unique_accounts)
        amount = round(RNG.uniform(10, 10000), 2)
        event_type = RNG.choice(['atm_withdrawal', 'pos_purchase', 'online_payment', 'transfer'])
        dt = random_timestamp(date(2025, 1, 1), date(2025, 12, 31))
        status = random.choices(['processed', 'pending', 'declined'], weights=[0.85, 0.10, 0.05], k=1)[0]
        events.append({
            "event_id": str(_deterministic_event_id(txn_id, idx)),
            "event_date": dt.date(),
            "event_hour": dt.hour,
            "transaction_id": str(txn_id),
            "account_id": account_id,
            "amount": amount,
            "event_type": event_type,
            "merchant_code": f"MC{RNG.randint(100,999)}",
            "location_lat": round(RNG.uniform(25, 48), 6),
            "location_lon": round(RNG.uniform(-125, -68), 6),
            "device_id": f"DEV{RNG.randint(1000,9999)}",
            "status": status,
            "processed_timestamp": dt,
            "ingestion_timestamp": dt + timedelta(seconds=RNG.randint(0, 60))
        })
    df = pd.DataFrame(events)
    if output_dir is not None:
        output_dir = os.fspath(output_dir)
    else:
        output_dir = "./data_output"
    for date_val, group in df.groupby('event_date'):
        partition_dir = os.path.join(output_dir, f"cassandra/event_date={date_val}")
        os.makedirs(partition_dir, exist_ok=True)
        try:
            group.to_parquet(os.path.join(partition_dir, "events.parquet"), index=False)
        except Exception:
            group.to_csv(os.path.join(partition_dir, "events.csv"), index=False)
    return df