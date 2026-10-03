-- Cassandra high-volume banking events DDL (mirrors
-- src/data_generation/init-scripts/cassandra/01_init.cql)
CREATE KEYSPACE IF NOT EXISTS banking_events
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

CREATE TABLE IF NOT EXISTS banking_events.account_events (
    event_id uuid,
    transaction_id text,
    account_id text,
    event_timestamp timestamp,
    event_type text,
    amount decimal,
    merchant_code text,
    location text,
    device_id text,
    status text,
    PRIMARY KEY ((account_id), event_timestamp, event_id)
) WITH CLUSTERING ORDER BY (event_timestamp DESC);

CREATE INDEX IF NOT EXISTS ix_event_type ON banking_events.account_events (event_type);
CREATE INDEX IF NOT EXISTS ix_event_status ON banking_events.account_events (status);