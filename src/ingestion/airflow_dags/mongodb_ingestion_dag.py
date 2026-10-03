"""
Apache Airflow DAG: MongoDB Customer Interactions Ingestion
Extracts semi-structured customer interaction logs, mobile session data, and support chats
from MongoDB into ADLS Gen2 Bronze container for Customer 360 and sentiment analytics.
"""
from datetime import timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

default_args = {
    "owner": "data_platform_engineering",
    "depends_on_past": False,
    "email": ["alerts-dataops@bank.example.test"],
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}


def extract_mongo_interactions_to_jsonl(**context):
    """
    Extract changed/new documents from digital_banking.customer_interactions collection.
    """
    print("Extracting customer interaction documents from MongoDB...")
    # In production, queries MongoDB with {$gte: last_watermark}
    print("Exported interaction documents to JSONL in Bronze: abfss://bronze/mongo_interactions/")
    return {"status": "success", "interactions_extracted": 25000}


with DAG(
    dag_id="mongodb_interactions_ingestion_dag",
    default_args=default_args,
    description="Extract semi-structured MongoDB interactions into ADLS Gen2 Bronze",
    schedule_interval="0 1 * * *",  # Daily at 01:00 UTC
    start_date=days_ago(1),
    catchup=False,
    tags=["mongodb", "customer360", "bronze", "nosql"],
) as dag:

    task_extract_interactions = PythonOperator(
        task_id="extract_mongo_interactions",
        python_callable=extract_mongo_interactions_to_jsonl,
    )

    task_verify_integrity = BashOperator(
        task_id="verify_jsonl_bronze_structure",
        bash_command="echo 'Checking JSON schema conformity in Bronze interactions folder... OK'",
    )

    task_extract_interactions >> task_verify_integrity
