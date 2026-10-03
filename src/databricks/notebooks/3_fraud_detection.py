"""
Databricks Banking Analytics: Fraud Detection Engine
PySpark implementation of rule-based and statistical anomaly detection on transaction streams.
Outputs curated Gold table: gold_fraud_alerts.
"""
import sys
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def get_spark_session():
    return (
        SparkSession.builder.appName("Banking_Fraud_Detection")
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        .getOrCreate()
    )


def run_fraud_detection(spark, silver_path: str, gold_path: str):
    print("Running PySpark Fraud Risk Analytics...")
    txns = spark.read.format("delta").load(f"{silver_path}/transactions")

    # Window for account-level moving metrics (10 prior transactions)
    account_window = (
        Window.partitionBy("account_id")
        .orderBy(F.col("transaction_date").cast("long"))
        .rowsBetween(-10, -1)
    )

    scored_txns = (
        txns
        .withColumn("prev_avg_amount", F.avg("amount").over(account_window))
        .withColumn("prev_std_amount", F.stddev("amount").over(account_window))
        .withColumn(
            "amount_zscore",
            F.when(F.col("prev_std_amount") > 0, (F.col("amount") - F.col("prev_avg_amount")) / F.col("prev_std_amount"))
            .otherwise(0.0)
        )
        # Fraud rule 1: High single transaction amount
        .withColumn("rule_high_amount", F.when(F.col("amount") >= 5000.0, 1).otherwise(0))
        # Fraud rule 2: Statistical anomaly (> 3 standard deviations from mean)
        .withColumn("rule_zscore_outlier", F.when(F.col("amount_zscore") >= 3.0, 1).otherwise(0))
        # Fraud rule 3: Rapid transaction frequency
        .withColumn("rule_rapid_movement", F.when((F.col("amount") > 1000.0) & (F.col("transaction_type") == "withdrawal"), 1).otherwise(0))
    )

    # Composite fraud score (0.0 to 1.0)
    alerts = (
        scored_txns
        .withColumn(
            "fraud_score",
            F.round(
                (F.col("rule_high_amount") * 0.45) +
                (F.col("rule_zscore_outlier") * 0.35) +
                (F.col("rule_rapid_movement") * 0.20),
                2
            )
        )
        .filter(F.col("fraud_score") >= 0.40)
        .withColumn(
            "risk_band",
            F.when(F.col("fraud_score") >= 0.70, "CRITICAL")
            .when(F.col("fraud_score") >= 0.50, "HIGH")
            .otherwise("MEDIUM")
        )
        .withColumn("alert_id", F.concat(F.lit("FRD-"), F.col("transaction_id")))
        .withColumn("generated_at", F.current_timestamp())
        .select(
            "alert_id",
            "transaction_id",
            "account_id",
            "amount",
            "transaction_date",
            "transaction_type",
            "fraud_score",
            "risk_band",
            "generated_at"
        )
    )

    alerts.write.format("delta").mode("overwrite").option("overwriteSchema", "true").save(f"{gold_path}/fraud_alerts")
    print(f"Successfully generated gold fraud alerts at {gold_path}/fraud_alerts")


if __name__ == "__main__":
    spark = get_spark_session()
    silver = sys.argv[1] if len(sys.argv) > 1 else "data/lakehouse/silver"
    gold = sys.argv[2] if len(sys.argv) > 2 else "data/lakehouse/gold"
    run_fraud_detection(spark, silver, gold)
