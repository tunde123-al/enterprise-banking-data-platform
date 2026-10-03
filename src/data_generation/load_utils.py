"""Shared safe CSV helpers for optional source-system loaders."""
import csv
from pathlib import Path


def csv_rows(output_dir, entity):
    with (Path(output_dir) / f"{entity}.csv").open(newline="", encoding="utf-8") as file:
        yield from csv.DictReader(file)


def insert_statement(table, columns, marker="?"):
    marks = ", ".join(f":{index}" for index, _ in enumerate(columns, 1)) if marker == ":" else ", ".join(marker for _ in columns)
    return f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({marks})"
