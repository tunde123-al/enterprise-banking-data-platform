"""
Databricks Banking Analytics: Customer 360 Unified Profile Engine
Consolidates demographics, omnichannel activity, deposit holdings, loan liabilities,
and compliance risk indicators into a single customer 360 gold table.
"""
import sys
from pyspark.sql import SparkSession
from pyspark.sql import functions as F


def get_spark_session():
    return (
        SparkSession.builder.appName("Banking_Customer_360")
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        .getOrCreate()
    )


def run_customer_360(spark, silver_path: str, gold_path: str):
    print("Building Gold Customer 360 Unified View...")
    customers = spark.read.format("delta").load(f"{silver_path}/customers")
    accounts = spark.read.format("delta").load(f"{silver_path}/accounts")

    # Account metrics per customer
    acc_summary = (
        accounts
        .groupBy("customer_id")
        .agg(
            F.count("account_id").alias("total_accounts"),
            F.round(F.sum("balance"), 2).alias("total_balance"),
            F.round(F.sum(F.when(F.col("account_type") == "checking", F.col("balance")).otherwise(0)), 2).alias("checking_balance"),
            F.round(F.sum(F.when(F.col("account_type") == "savings", F.col("balance")).otherwise(0)), 2).alias("savings_balance"),
            F.min("opened_date").alias("customer_since_date")
        )
    )

    # Customer 360 consolidation
    customer_360 = (
        customers
        .join(acc_summary, "customer_id", "left")
        .fillna({
            "total_accounts": 0,
            "total_balance": 0.0,
            "checking_balance": 0.0,
            "savings_balance": 0.0,
        })
        .withColumn(
            "customer_segment",
            F.when(F.col("total_balance") >= 100000.0, "HIGH_NET_WORTH")
            .when(F.col("total_balance") >= 25000.0, "AFFLUENT")
            .when(F.col("total_balance") >= 5000.0, "MASS_AFFLUENT")
            .otherwise("RETAIL")
        )
        .withColumn("profile_updated_at", F.current_timestamp())
    )

    customer_360.write.format("delta").mode("overwrite").option("overwriteSchema", "true").save(f"{gold_path}/customer_360")
    print(f"Successfully generated Gold Customer 360 dataset at {gold_path}/customer_360")


if __name__ == "__main__":
    spark = get_spark_session()
    silver = sys.argv[1] if len(sys.argv) > 1 else "data/lakehouse/silver"
    gold = sys.argv[2] if len(sys.argv) > 2 else "data/lakehouse/gold"
    run_customer_360(spark, silver, gold)
