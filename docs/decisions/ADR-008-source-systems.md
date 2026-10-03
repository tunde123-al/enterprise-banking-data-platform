# ADR-008: Heterogeneous source-system simulation

**Context:** demonstrate realistic banking integration patterns. **Decision:** map PostgreSQL to core banking, Oracle to legacy ledger, SQL Server to lending/branch, Azure SQL to digital app, MongoDB to interactions, Cassandra to high-volume events. **Alternatives:** one database or artificial equal workloads. **Consequences:** each technology has a business rationale; simulators may be schema-only when cost/time constrained.
