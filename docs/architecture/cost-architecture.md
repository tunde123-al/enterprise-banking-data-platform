# Cost architecture

The cost-sensitive MVP uses ADLS lifecycle policies, small auto-terminating Databricks job compute, scheduled ADF runs, and Synapse serverless or a paused/deleted dedicated pool. Avoid always-on clusters, unmanaged streaming, frequent full reloads, and unused private networking/capacity. Tag resources with `project`, `environment`, and `owner`; set budget alerts; stop/delete lab resources after demonstrations.

Potential cost hotspots are Databricks compute/DBUs, Synapse dedicated SQL, Data Factory activity/egress, Power BI licences/capacity, and network egress. Power BI Desktop is adequate for local development; publishing/sharing requires a suitable tenant/licence decision. Cost optimisation must not weaken the no-secrets or retention/backup baseline.
