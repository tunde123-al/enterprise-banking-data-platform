"""Load JSONL interactions into MongoDB (digital_banking.customer_interactions)."""
import json
import os
from pathlib import Path


def load(output_dir="data/generated"):
    from pymongo import MongoClient

    database = os.environ.get("MONGODB_DB", "digital_banking")
    with MongoClient(os.environ.get("MONGODB_URI", "mongodb://localhost:27017/")) as client, (
        Path(output_dir) / "interactions.jsonl"
    ).open(encoding="utf-8") as file:
        docs = [json.loads(line) for line in file if line.strip()]
        if docs:
            collection = client[database].customer_interactions
            collection.insert_many(docs, ordered=False)
            print(f"Loaded {len(docs)} interactions into {database}.customer_interactions")


if __name__ == "__main__":
    load()
