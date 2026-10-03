"""Load loan and repayment CSV files into Oracle Free (XEPDB1)."""
import argparse
import os
from datetime import datetime

from .load_utils import csv_rows, insert_statement

_NUMERIC_COLUMNS = {
    "principal_amount", "interest_rate", "current_balance", "term_months", "amount",
}
_DATE_COLUMNS = {
    "origination_date", "maturity_date", "created_date", "updated_date",
}
_TS_COLUMNS = {"payment_ts", "origination_ts"}


def _coerce(record):
    """Coerce CSV strings to Oracle-native Python types for a clean executemany."""
    coerced = []
    for key, value in record.items():
        if value == "" or value is None:
            coerced.append(None)
        elif key in _NUMERIC_COLUMNS:
            coerced.append(float(value))
        elif key in _DATE_COLUMNS:
            coerced.append(datetime.strptime(value[:10], "%Y-%m-%d").date())
        elif key in _TS_COLUMNS:
            coerced.append(datetime.fromisoformat(str(value).replace("Z", "+00:00")))
        else:
            coerced.append(value)
    return tuple(coerced)


def load(output_dir="data/generated"):
    import oracledb

    connection = oracledb.connect(
        user=os.environ["ORACLE_USER"],
        password=os.environ["ORACLE_PASSWORD"],
        dsn=os.environ["ORACLE_DSN"],
    )
    with connection, connection.cursor() as cursor:
        for table in ("loans", "repayments"):
            records = list(csv_rows(output_dir, table))
            if records:
                cursor.executemany(
                    insert_statement(table, records[0], ":"),
                    [_coerce(row) for row in records],
                )
    print("Oracle load complete.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default="data/generated")
    load(parser.parse_args().output_dir)
