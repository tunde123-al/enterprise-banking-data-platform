# Data generation strategy

`src/data_generation/generate_all.py` creates deterministic, fictional data with a fixed default seed. Generation order preserves foreign-key relationships: customers → accounts/loans/cards/devices/interactions; accounts → transactions/events; loans → repayments.

Default volumes are defined in `src/data_generation/generator_config.yaml`. Use smaller individual generator counts for local development, and retain the same seed for reproducible test cases.
