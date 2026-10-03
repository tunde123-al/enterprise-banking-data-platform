from pathlib import Path

from src.data_generation import generate_all


def test_generate_all_smoke(tmp_path):
    outputs = generate_all.main(output_dir=tmp_path, scale=0.001)

    expected = {
        "customers",
        "accounts",
        "transactions",
        "loans",
        "repayments",
        "cards",
        "merchants",
        "devices",
        "cassandra_events",
        "interactions",
        "fastapi_events",
    }
    assert set(outputs) == expected

    for path in outputs.values():
        assert Path(path).exists(), f"Missing generated output: {path}"
        assert Path(path).stat().st_size > 0, f"Empty output: {path}"


def test_fastapi_app_has_health_endpoint():
    from src.microservices.fastapi_app.main import app

    paths = {route.path for route in app.routes}
    assert "/health" in paths
