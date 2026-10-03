# Source-to-Bronze mapping

The Bronze layer stores each source payload unchanged, with these platform metadata fields appended: `ingestion_id`, `ingested_at_utc`, `source_system`, `source_entity`, `source_file`, and `record_hash`.

| Source entity | Bronze path | Incremental key |
|---|---|---|
| customers, accounts, loans, cards | `bronze/<source>/<entity>/snapshot_date=YYYY-MM-DD` | business key + snapshot date |
| transactions, repayments | `bronze/<source>/<entity>/event_date=YYYY-MM-DD` | transaction/repayment id |
| interactions, events | `bronze/<source>/<entity>/event_date=YYYY-MM-DD/hour=HH` | event/interaction id |

Reject malformed records to a quarantine path with the parsing error, original payload, and ingestion metadata. Do not silently drop source records.
