"""
Databricks Lakehouse Medallion Pipeline: Bronze to Silver Transformation
Reads raw ingestion data from Bronze, enforces schema, applies cleansing rules,
deduplicates records, and merges into conformed Delta Lake Silver tables.
"""
import sys
from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import (
    StructType, StructField, StringType, DoubleType,
    TimestampType, DateType, IntegerType, BooleanType
)
try:
    from delta.tables import DeltaTable
except ImportError:
    DeltaTable = None


def get_spark_session():
    """Create or get active Spark session with Delta Lake support."""
    builder = (
        SparkSession.builder.appName("Banking_Bronze_to_Silver")
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        .config("spark.sql.legacy.timeParserPolicy", "LEGACY")
    )
    return builder.getOrCreate()


def process_customers_bronze_to_silver(spark, bronze_path: str, silver_path: str):
    """Cleanse, deduplicate and merge Customers from Bronze into Silver."""
    print("Processing Customers: Bronze -> Silver...")
    raw_df = spark.read.format("csv").option("header", "true").load(f"{bronze_path}/customers.csv")

    clean_df = (
        raw_df
        .filter(F.col("customer_id").isNotNull())
        .withColumn("first_name", F.trim(F.initcap(F.col("first_name"))))
        .withColumn("last_name", F.trim(F.initcap(F.col("last_name"))))
        .withColumn("email", F.lower(F.trim(F.col("email"))))
        .withColumn("phone", F.regexp_replace(F.col("phone"), r"[^0-9+]", ""))
        .withColumn("kyc_tier", F.upper(F.col("kyc_tier")))
        .withColumn("status", F.upper(F.col("status")))
        .withColumn("country", F.upper(F.col("country")))
        .withColumn("silver_processed_at", F.current_timestamp())
        .dropDuplicates(["customer_id"])
    )

    clean_df.write.format("delta").mode("overwrite").option("overwriteSchema", "true").save(f"{silver_path}/customers")
    print(f"Successfully saved clean customers to {silver_path}/customers")


def process_accounts_bronze_to_silver(spark, bronze_path: str, silver_path: str):
    """Cleanse, deduplicate and write Accounts to Silver."""
    print("Processing Accounts: Bronze -> Silver...")
    raw_df = spark.read.format("csv").option("header", "true").load(f"{bronze_path}/accounts.csv")

    clean_df = (
        raw_df
        .filter(F.col("account_id").isNotNull())
        .withColumn("account_id", F.col("account_id").cast(StringType()))
        .withColumn("customer_id", F.col("customer_id").cast(StringType()))
        .withColumn("balance", F.round(F.col("balance").cast(DoubleType()), 2))
        .withColumn("available_balance", F.round(F.col("available_balance").cast(DoubleType()), 2))
        .withColumn("account_type", F.lower(F.trim(F.col("account_type"))))
        .withColumn("status", F.lower(F.trim(F.col("status"))))
        .withColumn("opened_date", F.to_date(F.col("opened_date")))
        .withColumn("closed_date", F.to_date(F.col("closed_date")))
        .withColumn("silver_processed_at", F.current_timestamp())
        .dropDuplicates(["account_id"])
    )

    clean_df.write.format("delta").mode("overwrite").option("overwriteSchema", "true").save(f"{silver_path}/accounts")
    print(f"Successfully saved clean accounts to {silver_path}/accounts")


def process_transactions_bronze_to_silver(spark, bronze_path: str, silver_path: str):
    """Cleanse, partition, and write Transactions into Silver Delta Lake."""
    print("Processing Transactions: Bronze -> Silver...")
    raw_df = spark.read.format("csv").option("header", "true").load(f"{bronze_path}/transactions.csv")

    clean_df = (
        raw_df
        .filter(F.col("transaction_id").isNotNull() & (F.col("amount").cast(DoubleType()) > 0))
        .withColumn("amount", F.round(F.col("amount").cast(DoubleType()), 2))
        .withColumn("balance_after", F.round(F.col("balance_after").cast(DoubleType()), 2))
        .withColumn("transaction_date", F.to_timestamp(F.col("transaction_date")))
        .withColumn("txn_year", F.year(F.col("transaction_date")))
        .withColumn("txn_month", F.month(F.col("transaction_date")))
        .withColumn("silver_processed_at", F.current_timestamp())
        .dropDuplicates(["transaction_id"])
    )

    clean_df.write.format("delta").partitionBy("txn_year", "txn_month").mode("overwrite").option("overwriteSchema", "true").save(f"{silver_path}/transactions")
    print(f"Successfully saved partitioned transactions to {silver_path}/transactions")


def process_loans_bronze_to_silver(spark, bronze_path: str, silver_path: str):
    """Cleanse and write Loans into Silver Delta Lake."""
    print("Processing Loans: Bronze -> Silver...")
    raw_df = spark.read.format("csv").option("header", "true").load(f"{bronze_path}/loans.csv")

    clean_df = (
        raw_df
        .filter(F.col("loan_id").isNotNull())
        .withColumn("principal_amount", F.round(F.col("principal_amount").cast(DoubleType()), 2))
        .withColumn("current_balance", F.round(F.col("current_balance").cast(DoubleType()), 2))
        .withColumn("interest_rate", F.round(F.col("interest_rate").cast(DoubleType()), 4))
        .withColumn("term_months", F.col("term_months").cast(IntegerType()))
        .withColumn("origination_date", F.to_date(F.col("origination_date")))
        .withColumn("maturity_date", F.to_date(F.col("maturity_date")))
        .withColumn("status", F.lower(F.trim(F.col("status"))))
        .withColumn("silver_processed_at", F.current_timestamp())
        .dropDuplicates(["loan_id"])
    )

    clean_df.write.format("delta").mode("overwrite").option("overwriteSchema", "true").save(f"{silver_path}/loans")
    print(f"Successfully saved clean loans to {silver_path}/loans")


def process_repayments_bronze_to_silver(spark, bronze_path: str, silver_path: str):
    """Cleanse and write Repayments into Silver Delta Lake."""
    print("Processing Repayments: Bronze -> Silver...")
    raw_df = spark.read.format("csv").option("header", "true").load(f"{bronze_path}/repayments.csv")

    clean_df = (
        raw_df
        .filter(F.col("repayment_id").isNotNull())
        .withColumn("amount", F.round(F.col("amount").cast(DoubleType()), 2))
        .withColumn("payment_ts", F.to_timestamp(F.col("payment_ts")))
        .withColumn("status", F.upper(F.trim(F.col("status"))))
        .withColumn("silver_processed_at", F.current_timestamp())
        .dropDuplicates(["repayment_id"])
    )

    clean_df.write.format("delta").mode("overwrite").option("overwriteSchema", "true").save(f"{silver_path}/repayments")
    print(f"Successfully saved clean repayments to {silver_path}/repayments")


def process_cards_bronze_to_silver(spark, bronze_path: str, silver_path: str):
    """Cleanse and write Cards into Silver Delta Lake (masked PAN only)."""
    print("Processing Cards: Bronze -> Silver...")
    raw_df = spark.read.format("csv").option("header", "true").load(f"{bronze_path}/cards.csv")

    clean_df = (
        raw_df
        .filter(F.col("card_id").isNotNull())
        .withColumn("card_type", F.upper(F.trim(F.col("card_type"))))
        .withColumn("status", F.upper(F.trim(F.col("status"))))
        .withColumn("silver_processed_at", F.current_timestamp())
        .dropDuplicates(["card_id"])
    )

    clean_df.write.format("delta").mode("overwrite").option("overwriteSchema", "true").save(f"{silver_path}/cards")
    print(f"Successfully saved clean cards to {silver_path}/cards")


def process_merchants_bronze_to_silver(spark, bronze_path: str, silver_path: str):
    """Cleanse and write Merchants into Silver Delta Lake."""
    print("Processing Merchants: Bronze -> Silver...")
    raw_df = spark.read.format("csv").option("header", "true").load(f"{bronze_path}/merchants.csv")

    clean_df = (
        raw_df
        .filter(F.col("merchant_id").isNotNull())
        .withColumn("merchant_name", F.trim(F.initcap(F.col("merchant_name"))))
        .withColumn("category_name", F.trim(F.initcap(F.col("category_name"))))
        .withColumn("country", F.upper(F.trim(F.col("country"))))
        .withColumn("silver_processed_at", F.current_timestamp())
        .dropDuplicates(["merchant_id"])
    )

    clean_df.write.format("delta").mode("overwrite").option("overwriteSchema", "true").save(f"{silver_path}/merchants")
    print(f"Successfully saved clean merchants to {silver_path}/merchants")


def process_devices_bronze_to_silver(spark, bronze_path: str, silver_path: str):
    """Cleanse and write Devices into Silver Delta Lake."""
    print("Processing Devices: Bronze -> Silver...")
    raw_df = spark.read.format("csv").option("header", "true").load(f"{bronze_path}/devices.csv")

    clean_df = (
        raw_df
        .filter(F.col("device_id").isNotNull())
        .withColumn("platform", F.upper(F.trim(F.col("platform"))))
        .withColumn("risk_score", F.round(F.col("risk_score").cast(DoubleType()), 4))
        .withColumn("trusted", F.col("trusted").cast(BooleanType()))
        .withColumn("silver_processed_at", F.current_timestamp())
        .dropDuplicates(["device_id"])
    )

    clean_df.write.format("delta").mode("overwrite").option("overwriteSchema", "true").save(f"{silver_path}/devices")
    print(f"Successfully saved clean devices to {silver_path}/devices")


def process_interactions_bronze_to_silver(spark, bronze_path: str, silver_path: str):
    """Cleanse and write Mongo JSONL interactions into Silver Delta Lake."""
    print("Processing Interactions: Bronze -> Silver...")
    raw_df = spark.read.format("json").load(f"{bronze_path}/interactions.jsonl")

    clean_df = (
        raw_df
        .filter(F.col("interaction_id").isNotNull() & F.col("customer_id").isNotNull())
        .withColumn("timestamp", F.to_timestamp(F.col("timestamp")))
        .withColumn("channel", F.upper(F.trim(F.col("channel"))))
        .withColumn("silver_processed_at", F.current_timestamp())
        .dropDuplicates(["interaction_id"])
    )

    clean_df.write.format("delta").mode("overwrite").option("overwriteSchema", "true").save(f"{silver_path}/interactions")
    print(f"Successfully saved clean interactions to {silver_path}/interactions")


def run_all_bronze_to_silver(bronze_dir="data/generated", silver_dir="data/lakehouse/silver"):
    """Orchestrate all Bronze to Silver transformations."""
    spark = get_spark_session()
    print("Starting Bronze to Silver Medallion Ingestion...")
    process_customers_bronze_to_silver(spark, bronze_dir, silver_dir)
    process_accounts_bronze_to_silver(spark, bronze_dir, silver_dir)
    process_transactions_bronze_to_silver(spark, bronze_dir, silver_dir)
    process_loans_bronze_to_silver(spark, bronze_dir, silver_dir)
    process_repayments_bronze_to_silver(spark, bronze_dir, silver_dir)
    process_cards_bronze_to_silver(spark, bronze_dir, silver_dir)
    process_merchants_bronze_to_silver(spark, bronze_dir, silver_dir)
    process_devices_bronze_to_silver(spark, bronze_dir, silver_dir)
    process_interactions_bronze_to_silver(spark, bronze_dir, silver_dir)
    print("Bronze to Silver Medallion run completed successfully.")


if __name__ == "__main__":
    bronze = sys.argv[1] if len(sys.argv) > 1 else "data/generated"
    silver = sys.argv[2] if len(sys.argv) > 2 else "data/lakehouse/silver"
    run_all_bronze_to_silver(bronze, silver)
