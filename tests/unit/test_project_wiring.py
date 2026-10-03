"""
Project-level wiring tests.

These tests fail fast when structural defects creep in and do not require any
external services (database, Spark, Airflow, Synapse). They cover:

- every Python file under src/ and tests/ parses (AST)
- every JSON definition parses (ADF pipelines, Databricks jobs, Synapse pipelines)
- every dbt {{ ref(...) }} / {{ source(...) }} target resolves in the project
- files referenced by documentation actually exist (Power BI scripts/DAX/RLS)
"""
import ast
import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]

PYTHON_DIRS = [
    ROOT / "src",
    ROOT / "tests",
]
JSON_GLOBS = [
    "src/**/*.json",
    "infrastructure/**/*.json",
]
DBT_DIR = ROOT / "src" / "dbt"
DBT_MODEL_GLOBS = [
    "staging/*.sql",
    "intermediate/*.sql",
    "dimensions/*.sql",
    "facts/*.sql",
    "marts/*.sql",
]


def _python_files():
    files = []
    for directory in PYTHON_DIRS:
        files.extend(directory.rglob("*.py"))
    return sorted(files)


def _json_files():
    files = []
    for pattern in JSON_GLOBS:
        files.extend(ROOT.glob(pattern))
    return sorted(files)


@pytest.mark.parametrize("path", _python_files(), ids=lambda p: str(p.relative_to(ROOT)))
def test_python_files_parse(path):
    """AST-parse every Python file so a syntax error never ships again."""
    ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


@pytest.mark.parametrize("path", _json_files(), ids=lambda p: str(p.relative_to(ROOT)))
def test_json_files_parse(path):
    """Every ADF / Databricks / Synapse JSON definition must be valid JSON."""
    json.loads(path.read_text(encoding="utf-8"))


def test_dbt_references_resolve():
    """Every {{ ref('model') }} and {{ source('name', 'table') }} must resolve."""
    model_files = []
    for pattern in DBT_MODEL_GLOBS:
        model_files.extend((DBT_DIR / "models").glob(pattern))

    models = {path.stem for path in model_files}

    # Sources are declared in models/staging/schema.yml
    schema_yml = (DBT_DIR / "models" / "staging" / "schema.yml").read_text(encoding="utf-8")
    sources = set(re.findall(r"^\s*- name:\s+(lakehouse_\w+)", schema_yml, re.MULTILINE))
    source_tables = set(re.findall(r"^\s*- name:\s+(\w+)", schema_yml, re.MULTILINE))

    unresolved_refs = []
    unknown_sources = []
    unknown_tables = []
    for path in model_files:
        text = path.read_text(encoding="utf-8")
        for ref in re.findall(r"\{\{\s*ref\('([^']+)'\)\s*\}\}", text):
            if ref not in models:
                unresolved_refs.append(f"{path.name}: ref('{ref}')")
        for source in re.findall(r"\{\{\s*source\('([^']+)'", text):
            if source not in sources:
                unknown_sources.append(f"{path.name}: source('{source}')")
        for table in re.findall(r"\{\{\s*source\('lakehouse_silver',\s*'([^']+)'\)\s*\}\}", text):
            if table not in source_tables:
                unknown_tables.append(f"{path.name}: source table '{table}'")

    assert not unresolved_refs, f"Unresolved dbt refs: {unresolved_refs}"
    assert not unknown_sources, f"Unknown dbt sources: {unknown_sources}"
    assert not unknown_tables, f"Unknown dbt source tables: {unknown_tables}"


def test_powerbi_documented_files_exist():
    """Files referenced by the Power BI README must exist on disk."""
    readme = (ROOT / "src" / "power_bi" / "README.md").read_text(encoding="utf-8")
    referenced = {
        "dax/measures.dax": ROOT / "src/power_bi/dax/measures.dax",
        "row_level_security.dax": ROOT / "src/power_bi/row_level_security.dax",
        "scripts/python_powerbi_segmentation.py": ROOT / "src/power_bi/scripts/python_powerbi_segmentation.py",
        "scripts/python_powerbi_anomaly_detection.py": ROOT / "src/power_bi/scripts/python_powerbi_anomaly_detection.py",
    }
    for label, path in referenced.items():
        assert path.is_file(), f"{label} is referenced in the README but missing: {path}"


def test_compose_and_dockerfile_present():
    """The local stack must be runnable from the repository root."""
    assert (ROOT / "docker-compose.yml").is_file()
    assert (ROOT / "Dockerfile.api").is_file()
    assert (ROOT / ".env.example").is_file()