"""Generate a referentially consistent set of synthetic banking source data."""
import argparse
from pathlib import Path

import yaml

from . import (
    generate_accounts,
    generate_cards,
    generate_cassandra_events,
    generate_customers,
    generate_devices,
    generate_fastapi_events,
    generate_interactions,
    generate_loans,
    generate_merchants,
    generate_repayments,
    generate_transactions,
)
from .core import DEFAULT_COUNTS, DEFAULT_OUTPUT_DIR, write_csv, write_jsonl
from .generator_utils import set_seed


def _load_config():
    config_path = Path(__file__).with_name("generator_config.yaml")
    with config_path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def main(output_dir=DEFAULT_OUTPUT_DIR, scale=1.0):
    output_dir = Path(output_dir)
    counts = {name: max(1, round(value * scale)) for name, value in DEFAULT_COUNTS.items()}
    config = _load_config()
    # Seed every PRNG (random, numpy, faker) for full reproducibility.
    set_seed(config["project"]["seed"])
    for key, value in counts.items():
        if key in config.get("volumes", {}):
            config["volumes"][key] = value

    customers = generate_customers.generate_customers(config)
    accounts = generate_accounts.generate_accounts(customers, config)
    merchants = generate_merchants.generate_merchants(config)
    loans = generate_loans.generate_loans(customers, accounts, config)
    transactions = generate_transactions.generate_transactions(accounts, merchants, config)

    outputs = {
        "customers": write_csv(customers, "customers", output_dir),
        "accounts": write_csv(accounts, "accounts", output_dir),
        "transactions": write_csv(transactions, "transactions", output_dir),
        "loans": write_csv(loans, "loans", output_dir),
        "repayments": write_csv(generate_repayments.generate(loans, count=counts["repayments"]), "repayments", output_dir),
        "cards": write_csv(generate_cards.generate(customers, count=counts["cards"]), "cards", output_dir),
        "merchants": write_csv(merchants, "merchants", output_dir),
        "devices": write_csv(generate_devices.generate(customers, count=counts["devices"]), "devices", output_dir),
        "cassandra_events": write_csv(generate_cassandra_events.generate_cassandra_events(transactions, config, output_dir), "cassandra_events", output_dir),
        "interactions": write_jsonl(generate_interactions.generate(customers, count=counts["interactions"]), "interactions", output_dir),
        "fastapi_events": write_jsonl(generate_fastapi_events.generate(accounts["account_id"].tolist(), count=counts["fastapi_events"]), "fastapi_events", output_dir),
    }
    return outputs


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument("--scale", type=float, default=1.0, help="Volume multiplier; use 0.001 for a quick local smoke test.")
    args = parser.parse_args()
    for name, path in main(args.output_dir, args.scale).items():
        print(f"{name}: {path}")
