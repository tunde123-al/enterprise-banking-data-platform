# ADR-009: Python and PySpark as transformation language

**Context:** the project needs portable data engineering and analytical code. **Decision:** use Python for generator/integration helpers and PySpark/Spark SQL for lakehouse transforms. **Alternatives:** Scala, Java, SQL-only. **Consequences:** accessible portfolio evidence and broad library support; enforce tests, style and dependency pinning.
