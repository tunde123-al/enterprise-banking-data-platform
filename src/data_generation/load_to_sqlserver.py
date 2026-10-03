"""Load card and merchant CSVs into SQL Server."""
import argparse, os
from .load_utils import csv_rows, insert_statement

def load(output_dir="data/generated", connection_string=None):
    import pyodbc
    with pyodbc.connect(connection_string or os.environ["SQLSERVER_CONNECTION_STRING"]) as connection:
        cursor = connection.cursor(); cursor.fast_executemany = True
        for table in ("cards", "merchants"):
            records = list(csv_rows(output_dir, table))
            if records: cursor.executemany(insert_statement(f"dbo.{table}", records[0]), [tuple(row.values()) for row in records])
        connection.commit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(); parser.add_argument("--output-dir", default="data/generated"); load(parser.parse_args().output_dir)
