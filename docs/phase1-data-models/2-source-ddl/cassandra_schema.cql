CREATE KEYSPACE IF NOT EXISTS banking_events WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};
CREATE TABLE IF NOT EXISTS banking_events.account_events (account_id text, event_ts timestamp, event_id uuid, event_type text, payload_version int, PRIMARY KEY ((account_id), event_ts, event_id)) WITH CLUSTERING ORDER BY (event_ts DESC);
