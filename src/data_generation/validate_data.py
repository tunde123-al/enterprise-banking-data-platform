"""
Comprehensive Data Quality & Validation Framework for Synthetic Banking Data.
Validates referential integrity, domain constraints, nullability, and formats.
"""
import argparse
import re
from pathlib import Path
import pandas as pd


def validate_customers(df: pd.DataFrame) -> dict:
    """Validate customer data against DQ rules."""
    results = {"total_records": len(df), "failures": []}
    
    # DQ-01: customer_id not null & unique
    if df['customer_id'].isnull().any():
        results["failures"].append("DQ-01 FAILED: Null customer_id found")
    if df['customer_id'].duplicated().any():
        results["failures"].append("DQ-01 FAILED: Duplicate customer_id found")

    # DQ-02: first_name & last_name not null
    if df['first_name'].isnull().any() or df['last_name'].isnull().any():
        results["failures"].append("DQ-02 FAILED: Null customer names found")

    # DQ-03: Email pattern format check
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    valid_emails = df['email'].dropna().apply(lambda x: bool(re.match(email_pattern, str(x))))
    email_pass_rate = valid_emails.mean() if len(valid_emails) > 0 else 1.0
    if email_pass_rate < 0.95:
        results["failures"].append(f"DQ-03 WARNING: Email format pass rate below 95% ({email_pass_rate:.1%})")

    # DQ-04: KYC Tier or Active status check
    if 'kyc_tier' in df.columns:
        valid_kyc = {"TIER_1", "TIER_2", "TIER_3"}
        invalid_kyc = set(df['kyc_tier'].dropna()) - valid_kyc
        if invalid_kyc:
            results["failures"].append(f"DQ-04 FAILED: Invalid kyc_tier values: {invalid_kyc}")
    elif 'is_active' in df.columns:
        if df['is_active'].isnull().any():
            results["failures"].append("DQ-04 FAILED: Null is_active found in customers")

    return results


def validate_accounts(df: pd.DataFrame, customers_df: pd.DataFrame = None) -> dict:
    """Validate accounts data and foreign key referential integrity."""
    results = {"total_records": len(df), "failures": []}

    # DQ-10: account_id unique and not null
    if df['account_id'].isnull().any() or df['account_id'].duplicated().any():
        results["failures"].append("DQ-10 FAILED: Invalid or duplicate account_id")

    # DQ-11: Referential integrity with customers
    if customers_df is not None:
        valid_cust_ids = set(customers_df['customer_id'])
        missing_custs = set(df['customer_id']) - valid_cust_ids
        if missing_custs:
            results["failures"].append(f"DQ-11 FAILED: {len(missing_custs)} accounts reference non-existent customer_ids")

    # DQ-12: Valid account types
    valid_types = {"checking", "savings", "money_market", "cd", "ira"}
    invalid_types = set(df['account_type'].dropna()) - valid_types
    if invalid_types:
        results["failures"].append(f"DQ-12 FAILED: Invalid account_types: {invalid_types}")

    return results


def validate_transactions(df: pd.DataFrame, accounts_df: pd.DataFrame = None) -> dict:
    """Validate transaction ledger records."""
    results = {"total_records": len(df), "failures": []}

    # DQ-20: transaction_id unique and not null
    if df['transaction_id'].isnull().any() or df['transaction_id'].duplicated().any():
        results["failures"].append("DQ-20 FAILED: Invalid or duplicate transaction_id")

    # DQ-21: Amount must be non-zero positive
    if (df['amount'] <= 0).any():
        results["failures"].append("DQ-21 FAILED: Non-positive transaction amounts found")

    # DQ-22: Referential integrity with accounts
    if accounts_df is not None:
        valid_acc_ids = set(accounts_df['account_id'])
        missing_accs = set(df['account_id']) - valid_acc_ids
        if missing_accs:
            results["failures"].append(f"DQ-22 FAILED: {len(missing_accs)} transactions reference unknown accounts")

    # DQ-23: Valid transaction types
    valid_txns = {"deposit", "withdrawal", "transfer", "payment", "fee"}
    invalid_txns = set(df['transaction_type'].dropna()) - valid_txns
    if invalid_txns:
        results["failures"].append(f"DQ-23 FAILED: Invalid transaction_types: {invalid_txns}")

    return results


def validate_all_datasets(data_dir: str = "data/generated") -> bool:
    """Run validation across all generated banking tables and files."""
    path = Path(data_dir)
    print(f"============================================================")
    print(f"Executing Data Quality & Validation Suite on {path}")
    print(f"============================================================")

    all_passed = True
    cust_df, acc_df, loans_df = None, None, None

    # Load Customers
    cust_file = path / "customers.csv"
    if cust_file.exists():
        cust_df = pd.read_csv(cust_file)
        res = validate_customers(cust_df)
        print(f"Customers ({res['total_records']} rows):")
        if res["failures"]:
            all_passed = False
            for f in res["failures"]: print(f"  [FAIL] {f}")
        else:
            print("  [PASS] All Customer DQ assertions passed.")

    # Load Accounts
    acc_file = path / "accounts.csv"
    if acc_file.exists():
        acc_df = pd.read_csv(acc_file)
        res = validate_accounts(acc_df, cust_df)
        print(f"Accounts ({res['total_records']} rows):")
        if res["failures"]:
            all_passed = False
            for f in res["failures"]: print(f"  [FAIL] {f}")
        else:
            print("  [PASS] All Account DQ assertions passed.")

    # Load Transactions
    txn_file = path / "transactions.csv"
    if txn_file.exists():
        txn_df = pd.read_csv(txn_file)
        res = validate_transactions(txn_df, acc_df)
        print(f"Transactions ({res['total_records']} rows):")
        if res["failures"]:
            all_passed = False
            for f in res["failures"]: print(f"  [FAIL] {f}")
        else:
            print("  [PASS] All Transaction DQ assertions passed.")

    print(f"============================================================")
    print(f"Overall Data Quality Status: {'PASSED [OK]' if all_passed else 'FAILED [X]'}")
    print(f"============================================================")
    return all_passed


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate generated banking data")
    parser.add_argument("--data-dir", default="data/generated")
    args = parser.parse_args()
    success = validate_all_datasets(args.data_dir)
    exit(0 if success else 1)