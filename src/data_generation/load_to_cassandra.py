"""Load Cassandra account event CSV into the banking_events keyspace."""
import os
import uuid
from datetime import datetime

from .load_utils import csv_rows


def _parse_timestamp(value):
    """Parse ISO-8601 / space-separated timestamps into a datetime object."""
    return datetime.fromisoformat(str(value).replace("Z", "+00:00"))


def load(output_dir="data/generated"):
    from cassandra.cluster import Cluster

    keyspace = os.environ.get("CASSANDRA_KEYSPACE", "banking_events")
    cluster = Cluster([os.environ.get("CASSANDRA_HOST", "localhost")])
    try:
        session = cluster.connect(keyspace)
        statement = session.prepare(
            "INSERT INTO account_events "
            "(event_id, transaction_id, account_id, event_timestamp, event_type, "
            " amount, merchant_code, location, device_id, status) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        )
        count = 0
        for row in csv_rows(output_dir, "cassandra_events"):
            location = f"{row.get('location_lat')},{row.get('location_lon')}"
            event_ts = _parse_timestamp(row["ingestion_timestamp"])
            session.execute(
                statement,
                (
                    uuid.UUID(row["event_id"]),
                    row.get("transaction_id"),
                    row["account_id"],
                    event_ts,
                    row["event_type"],
                    float(row["amount"]),
                    row.get("merchant_code"),
                    location,
                    row.get("device_id"),
                    row["status"],
                ),
            )
            count += 1
        print(f"Loaded {count} rows into {keyspace}.account_events")
    finally:
        cluster.shutdown()


if __name__ == "__main__":
    load()
