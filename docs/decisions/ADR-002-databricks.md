# ADR-002: Azure Databricks for scalable processing

**Context:** conformance and risk transformations require distributed PySpark. **Decision:** Databricks executes Bronze→Silver→Gold processing. **Alternatives:** ADF Mapping Data Flows, Synapse Spark, single-node Python. **Consequences:** strong Spark/Delta workflow and job orchestration; compute auto-termination is mandatory.
