# ADR-005: Airflow for code-centric event/document orchestration

**Context:** the portfolio should demonstrate open-source orchestration without duplicating ADF. **Decision:** use Airflow only for Python-first Cassandra/MongoDB/event flows and cross-tool examples. **Alternatives:** no Airflow, Airflow for all workflows. **Consequences:** clear demonstration role; additional operational surface and no duplicate schedules.
