# Data requirements

Every source record requires `source_system`, `ingest_batch_id`, `ingested_at_utc`, `record_hash`, and schema/version metadata in Bronze. Silver adds conformed identifiers, standard timestamps/currency/code values, quality status, and effective dating where required. Gold is product-oriented and excludes unneeded direct identifiers.

Customer, Account, Transaction, Card, Merchant, Loan, Repayment, Device, Interaction, AML Alert, Fraud Event, Risk, and Branch are mandatory domains. Business keys are retained for traceability; warehouse keys are surrogate integer/hash keys. Customer and branch dimensions use SCD Type 2 when attributes such as segment, residence region, or branch assignment change meaningfully.

Quality thresholds are configurable and recorded, not hard-coded claims: 100% primary-key uniqueness; 100% valid required relationship keys after quarantine; freshness/volume thresholds set per pipeline; monetary values non-negative unless a documented reversal; transaction timestamp not materially in future.
