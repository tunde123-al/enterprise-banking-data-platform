# ADR-007: Synapse as serving/warehouse layer

**Context:** BI users need SQL-accessible curated marts beyond raw lake data. **Decision:** use Synapse SQL capability where appropriate, with dbt-managed models. **Alternatives:** Databricks SQL only, Azure SQL, Power BI direct lake-only. **Consequences:** clear warehouse story; avoid dedicated capacity in MVP unless justified by load.
