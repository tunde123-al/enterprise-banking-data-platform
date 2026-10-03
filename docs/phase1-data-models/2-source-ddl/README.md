# Phase 1 source DDL (design reference)

The files in this folder are the **design-time** source-system definitions written during
Phase 1. They are condensed, illustrative and are **not executed** by anything in the
repository.

The executable, authoritative schemas are the container initialisation scripts in
[`src/data_generation/init-scripts/`](../../../src/data_generation/init-scripts), which
Docker Compose mounts into each database on first start. Where the two differ, the
init scripts take precedence: they are what the loaders in `src/data_generation/` run against.

| Design file here | Executable counterpart | Relationship |
| --- | --- | --- |
| `postgresql_ddl.sql` | `init-scripts/postgres/01_init.sql` | Design is narrower (fewer columns, `transaction_ts`/`direction`/`channel` naming) |
| `oracle_ddl.sql` | `init-scripts/oracle/01_init.sql` | Design is narrower |
| `sqlserver_ddl.sql` | `init-scripts/sqlserver/01_init.sql` | Design models `cards` + `merchants`; the init script creates `cards` + `devices` |
| `cassandra_ddl.cql` | `init-scripts/cassandra/01_init.cql` | Same table definition |
| `cassandra_schema.cql` | — | Earlier, simpler draft of the events table |
| `mongodb_indexes.js` | `init-scripts/mongodb/01_init.js` | Design indexes `interactions`/`devices`; the init script creates `customer_interactions` |
| `azuresql_ddl.sql` | — | No local container; Azure SQL is loaded through `load_to_azuresql.py` against a real instance |
