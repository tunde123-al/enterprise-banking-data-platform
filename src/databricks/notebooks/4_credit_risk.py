"""
Databricks Banking Analytics: Credit Risk & Delinquency Engine
Computes credit risk ratings, Debt-to-Balance ratios, default probabilities, and expected loss.
Outputs curated Gold table: gold_credit_risk_assessment.
"""
import sys
from pyspark.sql import SparkSession
from pyspark.sql import functions as F


def get_spark_session():
    return (
        SparkSession.builder.appName("Banking_Credit_Risk")
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        .getOrCreate()
    )


def run_credit_risk_assessment(spark, silver_path: str, gold_path: str):
    print("Running PySpark Credit Risk Models...")
    # Read loans (manufactured into Silver by the Bronze -> Silver job) and accounts
    loans = spark.read.format("delta").load(f"{silver_path}/loans")
    accounts = spark.read.format("delta").load(f"{silver_path}/accounts")

    # Aggregate customer total balances
    cust_balances = (
        accounts
        .groupBy("customer_id")
        .agg(F.sum("balance").alias("total_deposit_balance"))
    )

    credit_df = (
        loans
        .withColumn("principal_amount", F.col("principal_amount").cast("double"))
        .withColumn("interest_rate", F.col("interest_rate").cast("double"))
        .withColumn("term_months", F.col("term_months").cast("integer"))
        .join(cust_balances, "customer_id", "left")
        .fillna({"total_deposit_balance": 100.0})
        .withColumn(
            "debt_to_deposit_ratio",
            F.round(F.col("principal_amount") / F.greatest(F.col("total_deposit_balance"), F.lit(1.0)), 2)
        )
        # Probability of default approximation based on loan amount & coverage
        .withColumn(
            "probability_of_default",
            F.round(
                F.when(F.col("status") == "defaulted", 1.0)
                .when(F.col("debt_to_deposit_ratio") > 10.0, 0.25)
                .when(F.col("debt_to_deposit_ratio") > 5.0, 0.12)
                .when(F.col("debt_to_deposit_ratio") > 2.0, 0.05)
                .otherwise(0.02),
                4
            )
        )
        .withColumn(
            "credit_rating",
            F.when(F.col("probability_of_default") >= 0.50, "CCC")
            .when(F.col("probability_of_default") >= 0.20, "BB")
            .when(F.col("probability_of_default") >= 0.10, "BBB")
            .when(F.col("probability_of_default") >= 0.04, "A")
            .otherwise("AAA")
        )
        # Expected Loss (EL = PD * EAD * LGD, assuming 45% Loss Given Default)
        .withColumn("expected_loss", F.round(F.col("probability_of_default") * F.col("principal_amount") * 0.45, 2))
        .withColumn("assessed_at", F.current_timestamp())
    )

    credit_df.write.format("delta").mode("overwrite").option("overwriteSchema", "true").save(f"{gold_path}/credit_risk_assessment")
    print(f"Successfully generated credit risk assessments at {gold_path}/credit_risk_assessment")


if __name__ == "__main__":
    spark = get_spark_session()
    silver = sys.argv[1] if len(sys.argv) > 1 else "data/lakehouse/silver"
    gold = sys.argv[2] if len(sys.argv) > 2 else "data/lakehouse/gold"
    run_credit_risk_assessment(spark, silver, gold)
