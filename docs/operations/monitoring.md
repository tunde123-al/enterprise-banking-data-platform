# Monitoring and observability

Monitor ADF activity runs, Airflow DAG/task status, Databricks job/cluster/run metrics, Delta quality results, dbt tests, Synapse query/load outcomes, and Power BI refreshes. Every pipeline reports execution status, duration, records read/written/rejected, watermark, data freshness, quality failures, and a correlation/run ID.

Alert on repeated failures, missing expected arrival, material volume deviation, failed quality gate, failed Power BI refresh, and cost/compute threshold. Azure Monitor and Log Analytics are the primary Azure aggregation layer; Airflow/Databricks native logs remain the diagnostic source. Dashboard health is separate from business dashboards.
