"""Shared, deterministic helpers for the synthetic source-system generators."""
from __future__ import annotations

import csv
import json
import random
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Iterable, Mapping

DEFAULT_OUTPUT_DIR = Path("data/generated")
DEFAULT_SEED = 20260817
DEFAULT_COUNTS = {
    "customers": 200_000, "accounts": 1_000_000, "transactions": 10_000_000,
    "loans": 50_000, "repayments": 200_000, "cards": 50_000, "merchants": 5_000,
    "interactions": 1_000_000, "devices": 200_000, "cassandra_events": 5_000_000,
    "fastapi_events": 100,
}


def rng(seed: int = DEFAULT_SEED, salt: int = 0) -> random.Random:
    return random.Random(seed + salt)


def uid(prefix: str, number: int) -> str:
    return f"{prefix}{number:08d}"


def timestamp(randomizer: random.Random, days: int = 365) -> str:
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=days)
    return (start + timedelta(seconds=randomizer.randrange(int((end - start).total_seconds())))).isoformat()


def write_csv(rows: Iterable[Mapping[str, object]], name: str, output_dir: Path = DEFAULT_OUTPUT_DIR) -> Path:
    if hasattr(rows, "to_dict"):
        rows = rows.to_dict(orient="records")
    rows = list(rows)
    path = output_dir / f"{name}.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return path
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    return path


def write_jsonl(rows: Iterable[Mapping[str, object]], name: str, output_dir: Path = DEFAULT_OUTPUT_DIR) -> Path:
    if hasattr(rows, "to_dict"):
        rows = rows.to_dict(orient="records")
    path = output_dir / f"{name}.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, default=str) + "\n")
    return path


def event_id() -> str:
    return str(uuid.uuid4())
