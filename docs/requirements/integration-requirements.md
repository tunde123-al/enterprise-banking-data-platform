# Integration requirements

ADF owns scheduled relational copy from PostgreSQL, Oracle, SQL Server, and Azure SQL into ADLS. Airflow owns code-defined MongoDB/Cassandra/event ingestion and cross-step orchestration where Python operators provide value. Both must emit a common ingestion manifest and use safe retry/idempotency semantics. Databricks is invoked only after landing validation succeeds.

No system passes passwords in pipeline code. Source extracts are read-only and synthetic. Schema changes require contract versioning; additive fields may be accepted after review, while incompatible changes fail/quarantine and raise an incident. API integration is optional and limited to synthetic FastAPI event generation.
