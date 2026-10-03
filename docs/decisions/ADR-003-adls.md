# ADR-003: ADLS Gen2 as lake storage

**Context:** the platform requires inexpensive zone-based storage and access controls. **Decision:** use ADLS Gen2 for landing, Bronze, Silver, Gold and checkpoints. **Alternatives:** Blob-only, database staging, S3/GCS. **Consequences:** hierarchical namespace/ACLs and Azure integration; lifecycle controls are needed.
