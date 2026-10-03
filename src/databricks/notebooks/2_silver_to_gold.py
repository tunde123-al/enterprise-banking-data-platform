"""
Databricks Lakehouse Medallion Pipeline: Silver to Gold Curated Aggregations
Computes business-level analytical marts, executive KPIs, and daily account metrics.
Exposes curated Delta Lake tables for Power BI and Synapse SQL consumption.
"""
import sys
from pyspark.sql import SparkSession
from pyspark.sql import functions as F


def get_spark_session():
    return (
        SparkSession.builder.appName("Banking_Silver_to_Gold")
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        .getOrCreate()
    )


def build_daily_account_metrics(spark, silver_path: str, gold_path: str):
    """Aggregate daily transaction activity by account."""
    print("Building Gold Daily Account Metrics...")
    txns = spark.read.format("delta").load(f"{silver_path}/transactions")

    daily_metrics = (
        txns.withColumn("txn_date", F.to_date("transaction_date"))
        .groupBy("account_id", "txn_date")
        .agg(
            F.count("transaction_id").alias("transaction_count"),
            F.sum(F.when(F.col("transaction_type") == "deposit", F.col("amount")).otherwise(0)).alias("total_deposits"),
            F.sum(F.when(F.col("transaction_type") != "deposit", F.col("amount")).otherwise(0)).alias("total_withdrawals"),
            F.round(F.sum("amount"), 2).alias("total_volume"),
            F.round(F.avg("amount"), 2).alias("average_transaction_amount"),
            F.max("balance_after").alias("end_of_day_balance"),
        )
        .withColumn("gold_updated_at", F.current_timestamp())
    )

    daily_metrics.write.format("delta").mode("overwrite").option("overwriteSchema", "true").save(f"{gold_path}/daily_account_metrics")
    print(f"Saved daily account metrics to {gold_path}/daily_account_metrics")


def build_executive_kpis(spark, silver_path: str, gold_path: str):
    """Compute executive-level overview metrics across customers, accounts, and volume."""
    print("Building Gold Executive KPIs...")
    customers = spark.read.format("delta").load(f"{silver_path}/customers")
    accounts = spark.read.format("delta").load(f"{silver_path}/accounts")
    txns = spark.read.format("delta").load(f"{silver_path}/transactions")

    exec_summary = (
        customers.join(accounts, "customer_id", "inner")
        .groupBy("country", "kyc_tier", "account_type")
        .agg(
            F.countDistinct("customer_id").alias("total_customers"),
            F.countDistinct("account_id").alias("total_accounts"),
            F.round(F.sum("balance"), 2).alias("total_deposits_balance"),
            F.round(F.avg("balance"), 2).alias("average_account_balance"),
        )
        .withColumn("calculated_date", F.current_date())
    )

    exec_summary.write.format("delta").mode("overwrite").option("overwriteSchema", "true").save(f"{gold_path}/executive_kpis")
    print(f"Saved executive KPIs to {gold_path}/executive_kpis")


def run_all_silver_to_gold(silver_dir="data/lakehouse/silver", gold_dir="data/lakehouse/gold"):
    spark = get_spark_session()
    print("Starting Silver to Gold Curated Aggregations...")
    build_daily_account_metrics(spark, silver_dir, gold_dir)
    build_executive_kpis(spark, silver_dir, gold_dir)
    print("Silver to Gold Medallion run completed successfully.")


if __name__ == "__main__":
    silver = sys.argv[1] if len(sys.argv) > 1 else "data/lakehouse/silver"
    gold = sys.argv[2] if len(sys.argv) > 2 else "data/lakehouse/gold"
    run_all_silver_to_gold(silver, gold)
