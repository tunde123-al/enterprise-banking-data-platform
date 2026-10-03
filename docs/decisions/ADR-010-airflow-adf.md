# ADR-010: Airflow and ADF responsibility boundary

**Context:** two orchestration tools can create competing ownership. **Decision:** ADF owns scheduled relational movement; Airflow owns code/event/document demonstrations; shared audit contract and explicit trigger ownership prevent duplication. **Alternatives:** both orchestrate all pipelines, select only one. **Consequences:** MVP can run ADF-only for minimum cost while retaining an Airflow showcase path; a workflow has one primary scheduler.
