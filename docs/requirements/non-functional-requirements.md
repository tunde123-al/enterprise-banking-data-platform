# Non-functional requirements

| Area | Requirement | Release |
| --- | --- | --- |
| Performance | Daily MVP batch completes within a developer-defined window; record actual baseline and target, do not claim enterprise SLA. | MVP |
| Scalability | Partition large transaction/event Delta tables and use incremental loads/merges. | MVP |
| Reliability | Pipelines are idempotent, retry transient failures, audit batches, and support restart. | MVP |
| Availability | Portfolio services are best-effort, not 24×7. | MVP |
| Security | Entra/RBAC, managed identity, Key Vault, TLS, encryption, and no secrets in Git. | MVP |
| Observability | Capture status, duration, counts, rejects, failures, freshness, and quality outcomes. | MVP |
| Maintainability | Versioned configuration, runbooks, tests, ADRs, and data contracts. | MVP |
| Interoperability | Use Parquet/Delta and documented SQL/API data contracts. | MVP |
| Recoverability | RPO ≤24 h, RTO ≤1 business day target for synthetic batch environment. | MVP |
| High availability/DR | regional resilience, formal tested RTO/RPO, and capacity design. | Production extension |
