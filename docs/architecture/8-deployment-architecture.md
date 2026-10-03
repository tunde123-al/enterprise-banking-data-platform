# Deployment architecture

Infrastructure is declarative (Terraform or ARM, choose one as the deployable source of truth). Pipeline definitions, notebooks, dbt project, SQL scripts, and documentation are version controlled. CI validates formatting, unit/data-contract tests, security scanning, and plan output; CD deploys to non-production using managed identity and approvals. Configuration is environment-specific; secrets are Key Vault references only.

Deployment order: foundation (resource groups/network/identity) → storage and Key Vault → ADF/Databricks/Synapse → ingestion/transformation assets → dbt/semantic model configuration → monitoring alerts. Roll back declarative infrastructure cautiously; data pipelines roll forward with idempotent reruns and Delta version recovery.
