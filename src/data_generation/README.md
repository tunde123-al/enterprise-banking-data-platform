# Synthetic source data

Run the full deterministic dataset generator from the repository root (the default produces the configured production-scale volumes):

```bash
python -m src.data_generation.generate_all
```

For a quick local dataset, use a scale multiplier and validate it afterwards:

```bash
python -m src.data_generation.generate_all --scale 0.001
python -m src.data_generation.validate_data
```

Outputs are written to `data/generated/`. CSV represents relational and Cassandra load inputs; JSONL represents MongoDB interaction and real-time API event streams. The default seed and volumes are recorded in `generator_config.yaml`; individual generators accept `count` and `seed` arguments for smaller test runs. Database loaders require their matching connection-string environment variable and the optional packages in `requirements_generation.txt`.

The generators intentionally use fictional `example.test` identities and masked card numbers. They do not produce real customer data or full PANs.
