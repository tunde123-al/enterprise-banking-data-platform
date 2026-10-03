# ADR-004: Delta Lake table format

**Context:** batch reruns and incremental updates need reliable table semantics. **Decision:** store curated lake layers as Delta tables. **Alternatives:** CSV/JSON, plain Parquet, Iceberg. **Consequences:** ACID merges, schema enforcement and time travel; requires compatible compute and maintenance.
