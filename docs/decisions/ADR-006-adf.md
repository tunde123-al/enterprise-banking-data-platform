# ADR-006: ADF for Azure-native relational ingestion

**Context:** relational sources benefit from managed connectors and copy monitoring. **Decision:** ADF owns scheduled relational extraction/landing and may trigger a downstream job after success. **Alternatives:** Airflow-only, custom Python. **Consequences:** less custom connector code; pipeline JSON/release management required.
