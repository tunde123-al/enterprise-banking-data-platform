"""
Databricks Banking Analytics: Anti-Money Laundering (AML) Monitoring Engine
Detects transaction structuring (smurfing below $10k threshold), rapid movement of funds,
and generates SAR (Suspicious Activity Report) candidates.
Outputs curated Gold table: gold_aml_alerts.
"""
import sys
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def get_spark_session():
    return (
        SparkSession.builder.appName("Banking_AML_Monitoring")
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        .getOrCreate()
    )


def run_aml_monitoring(spark, silver_path: str, gold_path: str):
    print("Running PySpark AML Rule Engine & Suspicious Activity Detection...")
    txns = spark.read.format("delta").load(f"{silver_path}/transactions")

    # 1. Structuring Rule: Transactions between $8,500 and $9,999 (attempting to evade $10k CTR filing)
    structuring_df = (
        txns
        .filter((F.col("amount") >= 8500.0) & (F.col("amount") < 10000.0))
        .withColumn("aml_rule", F.lit("AML_STRUCTURING_SUB_10K"))
        .withColumn("risk_score", F.lit(0.85))
    )

    # 2. Large Cash / Transfer Rule: Single transaction exceeding $25,000
    large_movement_df = (
        txns
        .filter(F.col("amount") >= 25000.0)
        .withColumn("aml_rule", F.lit("AML_HIGH_VALUE_CTR"))
        .withColumn("risk_score", F.lit(0.70))
    )

    # Union alerts
    all_aml_alerts = (
        structuring_df.unionByName(large_movement_df, allowMissingColumns=True)
        .withColumn("aml_alert_id", F.concat(F.lit("AML-"), F.col("transaction_id")))
        .withColumn("sar_recommended", F.when(F.col("risk_score") >= 0.80, True).otherwise(False))
        .withColumn("flagged_timestamp", F.current_timestamp())
        .select(
            "aml_alert_id",
            "transaction_id",
            "account_id",
            "amount",
            "transaction_type",
            "transaction_date",
            "aml_rule",
            "risk_score",
            "sar_recommended",
            "flagged_timestamp"
        )
    )

    all_aml_alerts.write.format("delta").mode("overwrite").option("overwriteSchema", "true").save(f"{gold_path}/aml_alerts")
    print(f"Successfully generated AML monitoring alerts at {gold_path}/aml_alerts")


if __name__ == "__main__":
    spark = get_spark_session()
    silver = sys.argv[1] if len(sys.argv) > 1 else "data/lakehouse/silver"
    gold = sys.argv[2] if len(sys.argv) > 2 else "data/lakehouse/gold"
    run_aml_monitoring(spark, silver, gold)
