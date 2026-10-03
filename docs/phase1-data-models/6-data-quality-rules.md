# Source data quality rules

1. Primary identifiers must be present and unique within an extract.
2. Foreign keys must resolve to a parent record in the same batch or a retained master snapshot.
3. Monetary amounts must be non-negative and currency must be ISO 4217.
4. Event timestamps must be UTC, parseable, and not materially in the future.
5. Status and product fields must belong to the documented controlled value set.
6. Customer email and phone are PII: mask or tokenize outside controlled zones.
7. Card values must be masked; full PAN/CVV must be rejected.
