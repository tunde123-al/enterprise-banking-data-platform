# Disaster recovery

This is a pragmatic portfolio DR design: raw immutable data and infrastructure definitions are recoverable; running compute is disposable; pipelines have retries and restart points. Target objectives are illustrative, not contractual: RPO ≤24 hours for batch data and RTO ≤1 business day for the portfolio environment.

| Failure | Recovery approach |
| --- | --- |
| copy/pipeline failure | retry transient faults; rerun by idempotent batch ID; inspect audit log |
| bad transformation | quarantine, correct code, rerun; restore Delta table version where appropriate |
| source/database loss | regenerate synthetic source data or use database backup/export |
| workspace/infrastructure loss | redeploy declared infrastructure; restore artifacts from private Git repository |
| accidental BI change | restore semantic/report version from source-controlled artefacts where available |

Checkpoint paths, Delta history, ingestion manifests, and run IDs make restart/reconciliation possible. Test recovery with an intentional failed batch and a Delta rollback exercise before presenting the project.
