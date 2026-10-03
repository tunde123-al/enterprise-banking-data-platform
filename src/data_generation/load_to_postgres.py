"""
Load generated banking data into PostgreSQL Core Banking Database.
"""
import argparse
import os
from pathlib import Path
import psycopg2
from psycopg2.extras import execute_values
import pandas as pd
import yaml


def get_connection(config=None):
    """Establish connection to PostgreSQL."""
    host = os.environ.get("POSTGRES_HOST", "localhost")
    port = os.environ.get("POSTGRES_PORT", "5432")
    db = os.environ.get("POSTGRES_DB", "core_banking")
    user = os.environ.get("POSTGRES_USER", "bankadmin")
    # The password comes from the environment only (see .env.example).
    password = os.environ["POSTGRES_PASSWORD"]

    if config and "database_connection" in config and "postgres" in config["database_connection"]:
        pg_cfg = config["database_connection"]["postgres"]
        host = pg_cfg.get("host", host)
        port = pg_cfg.get("port", port)
        db = pg_cfg.get("database", db)
        user = pg_cfg.get("user", user)

    return psycopg2.connect(
        host=host,
        port=port,
        database=db,
        user=user,
        password=password,
    )


def load_table(conn, table_name: str, df: pd.DataFrame, batch_size: int = 5000):
    """Insert DataFrame into PostgreSQL table using execute_values batching."""
    if df.empty:
        print(f"Skipping {table_name} (no data)")
        return

    cursor = conn.cursor()
    columns = list(df.columns)
    col_str = ", ".join(columns)
    sql = f"INSERT INTO {table_name} ({col_str}) VALUES %s ON CONFLICT DO NOTHING;"

    # Blank CSV cells arrive as NaN; send them as SQL NULL.
    df = df.astype(object).where(df.notna(), None)
    records = [tuple(x) for x in df.to_numpy()]
    execute_values(cursor, sql, records, page_size=batch_size)
    conn.commit()
    cursor.close()
    print(f"Loaded {len(df)} rows into {table_name}")


def load_all_postgres(data_dir: str = "data/generated", config_path: str = None):
    """Load customers, accounts, merchants, and transactions into Postgres."""
    cfg = None
    if config_path and Path(config_path).exists():
        with open(config_path, "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f)

    data_path = Path(data_dir)
    print(f"Connecting to PostgreSQL and loading from {data_path}...")

    conn = get_connection(cfg)
    try:
        # 1. Customers
        cust_file = data_path / "customers.csv"
        if cust_file.exists():
            df_cust = pd.read_csv(cust_file, dtype=str)
            load_table(conn, "core_banking.customers", df_cust)

        # 2. Merchants
        merch_file = data_path / "merchants.csv"
        if merch_file.exists():
            df_merch = pd.read_csv(merch_file, dtype=str)
            load_table(conn, "core_banking.merchants", df_merch)

        # 3. Accounts
        acc_file = data_path / "accounts.csv"
        if acc_file.exists():
            df_acc = pd.read_csv(acc_file, dtype=str)
            load_table(conn, "core_banking.accounts", df_acc)

        # 4. Transactions
        txn_file = data_path / "transactions.csv"
        if txn_file.exists():
            df_txn = pd.read_csv(txn_file, dtype=str)
            load_table(conn, "core_banking.transactions", df_txn)

        print("PostgreSQL loading complete.")
    finally:
        conn.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Load data to PostgreSQL")
    parser.add_argument("--data-dir", default="data/generated", help="Directory containing generated CSV files")
    parser.add_argument("--config", default="src/data_generation/generator_config.yaml", help="Path to config YAML")
    args = parser.parse_args()

    load_all_postgres(args.data_dir, args.config)