# Network architecture

The portfolio implementation keeps the topology small: managed Azure services live in one region; VNet integration/private endpoints protect data-plane access; public ingress is disabled or restricted where supported. Developer access uses Entra authentication, never exposed database credentials.

```mermaid
flowchart LR
U[Engineer / analyst via Entra] --> CP[Azure control plane]
subgraph VNet
 IR[ADF managed VNet / integration] --> PE[Private endpoints]
 DB[Databricks private / delegated subnet] --> PE
end
PE --> D[ADLS • Key Vault • Azure SQL • Synapse]
P[Power BI Service] -->|approved cloud connector / gateway if required| D
```

Production adds private DNS, firewall policy, egress control, split development/test/production subscriptions, and connectivity to on-premises sources.
