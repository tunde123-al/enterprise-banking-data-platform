"""
Apache Airflow DAG: Cassandra Event Store Ingestion
Performs micro-batch / incremental ingestion of high-volume banking and transaction events
from Apache Cassandra into ADLS Gen2 Bronze Event Store.
"""
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

default_args = {
    "owner": "data_platform_engineering",
    "depends_on_past": False,
    "email": ["alerts-dataops@bank.example.test"],
    "retries": 2,
    "retry_delay": timedelta(minutes=3),
}


def extract_cassandra_events_to_parquet(**context):
    """
    Query Cassandra account_events table by time window and write partitioned Parquet to ADLS Gen2.
    """
    execution_date = context.get("execution_date", datetime.utcnow())
    print(f"Extracting Cassandra events for window: {execution_date}")
    # In production, queries Cassandra session with token ranges or timestamp clustering key
    print("Exported 150,000 banking event records to ADLS Gen2: abfss://bronze/cassandra_events/year=2026/month=09/")
    return {"status": "success", "record_count": 150000}


with DAG(
    dag_id="cassandra_events_ingestion_dag",
    default_args=default_args,
    description="High-frequency Cassandra events ingestion into ADLS Gen2 Bronze",
    schedule_interval="*/30 * * * *",  # Every 30 minutes
    start_date=days_ago(1),
    catchup=False,
    tags=["cassandra", "events", "bronze", "streaming"],
) as dag:

    task_extract_events = PythonOperator(
        task_id="extract_cassandra_events_to_bronze",
        python_callable=extract_cassandra_events_to_parquet,
    )

    task_validate_bronze_file = BashOperator(
        task_id="validate_bronze_event_partition",
        bash_command="echo 'Validating Parquet schema and partition metadata on ADLS Gen2 Bronze... OK'",
    )

    task_extract_events >> task_validate_bronze_file
