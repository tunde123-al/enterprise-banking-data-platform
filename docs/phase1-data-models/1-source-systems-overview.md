# Phase 1 source systems

| Source | Data domains | Landing format |
|---|---|---|
| PostgreSQL | customers, accounts, transactions | CSV / JDBC |
| Oracle | loans, repayments | CSV / JDBC |
| SQL Server / Azure SQL | cards, merchants | CSV / JDBC |
| MongoDB | customer interactions, devices | JSONL |
| Cassandra | high-volume account events | CSV / CQL |
| FastAPI | real-time transaction alerts | JSONL / HTTP |

Every record has a stable business key. Event sources include an event identifier and UTC timestamp to support replay, deduplication, and lineage.
