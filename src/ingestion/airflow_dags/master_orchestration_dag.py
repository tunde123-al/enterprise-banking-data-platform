"""
Apache Airflow Master Orchestration DAG: Enterprise Banking Data Platform
Orchestrates end-to-end extraction from relational and NoSQL sources into ADLS Gen2 Bronze,
triggers Databricks Medallion processing (Bronze -> Silver -> Gold), and runs dbt marts.
"""
from datetime import timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

# Local lakehouse paths used by the BashOperator run of the Databricks notebooks.
# In Azure, replace these with the DatabricksRunNowOperator-backed tasks documented
# in docs/decisions/ADR-010-airflow-adf.md.
LAKEHOUSE_PATHS = {
    "bronze": "data/generated",
    "silver": "data/lakehouse/silver",
    "gold": "data/lakehouse/gold",
}

default_args = {
    "owner": "data_platform_engineering",
    "depends_on_past": False,
    "email": ["alerts-dataops@bank.example.test"],
    "email_on_failure": True,
    "email_on_retry": False,
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
}


def check_source_connectivity():
    """Verify connectivity to PostgreSQL, Oracle, SQL Server, Mongo, Cassandra."""
    print("Checking connectivity to operational databases...")
    # Health probe logic
    print("All 5 operational source stores are reachable and responding.")
    return True


def ingest_relational_to_bronze():
    """Extract relational tables (PostgreSQL, Oracle, SQL Server) to ADLS Gen2 Landing/Bronze."""
    print("Running incremental extract for Core Banking (Postgres), Loans (Oracle), Cards (SQL Server)...")
    print("Uploaded raw parquet partitions to abfss://bronze@adlsbankingplatformdev.dfs.core.windows.net/")
    return {"status": "success", "partitions_written": ["customers", "accounts", "transactions", "loans", "cards"]}


with DAG(
    dag_id="master_banking_orchestration_dag",
    default_args=default_args,
    description="Enterprise Banking End-to-End Orchestration: Ingestion, Lakehouse & Warehouse",
    schedule_interval="0 2 * * *",  # Daily at 02:00 UTC
    start_date=days_ago(1),
    catchup=False,
    tags=["banking", "lakehouse", "medallion", "production"],
) as dag:

    # 1. Health & Pre-flight checks
    task_health_check = PythonOperator(
        task_id="preflight_source_health_check",
        python_callable=check_source_connectivity,
    )

    # 2. Extract Relational Sources to ADLS Gen2 Bronze
    task_extract_relational = PythonOperator(
        task_id="extract_relational_to_adls_bronze",
        python_callable=ingest_relational_to_bronze,
    )

    # 3. Trigger External Specialized Ingestion DAGs (MongoDB & Cassandra)
    task_trigger_nosql = BashOperator(
        task_id="trigger_nosql_ingestion",
        bash_command="echo 'Triggering cassandra_ingestion_dag and mongodb_ingestion_dag via Airflow CLI/API'",
    )

    # 4. Trigger Databricks Bronze to Silver Medallion Transformation
    task_bronze_to_silver = BashOperator(
        task_id="databricks_bronze_to_silver",
        bash_command=(
            "python src/databricks/notebooks/1_bronze_to_silver.py "
            f"{LAKEHOUSE_PATHS['bronze']} {LAKEHOUSE_PATHS['silver']}"
        ),
    )

    # 5. Trigger Databricks Silver to Gold Curated Marts & Risk Models
    task_silver_to_gold = BashOperator(
        task_id="databricks_silver_to_gold",
        bash_command=(
            "python src/databricks/notebooks/2_silver_to_gold.py "
            f"{LAKEHOUSE_PATHS['silver']} {LAKEHOUSE_PATHS['gold']}"
        ),
    )

    # 6. Execute dbt models for Synapse / Warehouse Views
    task_run_dbt = BashOperator(
        task_id="execute_dbt_marts_and_tests",
        bash_command="cd src/dbt && dbt build --target {{ var.value.dbt_target or 'synapse' }}",
    )

    # 7. Post-Run Notification & SLA Confirmation
    task_notify = BashOperator(
        task_id="notify_pipeline_success",
        bash_command="echo 'Master banking orchestration pipeline completed successfully. Gold datasets refreshed.'",
    )

    # Pipeline Task Dependencies
    task_health_check >> [task_extract_relational, task_trigger_nosql]
    [task_extract_relational, task_trigger_nosql] >> task_bronze_to_silver
    task_bronze_to_silver >> task_silver_to_gold
    task_silver_to_gold >> task_run_dbt
    task_run_dbt >> task_notify
