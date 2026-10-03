# Security architecture

The MVP follows a production-inspired zero-trust baseline: Microsoft Entra ID authenticates people and workloads; RBAC and data ACLs authorize least privilege; managed identities access Azure services; Key Vault stores deploy-time secrets; TLS protects traffic and platform encryption protects stored data. Private endpoints and restricted public access are preferred for deployed data services.

| Control | Portfolio implementation | Production extension |
| --- | --- | --- |
| Identity | Entra groups: platform-admin, engineer, analyst, auditor | privileged identity management and conditional access |
| Secrets | Key Vault references; `.env` excluded | rotation policies, HSM-backed keys |
| Data access | ADLS ACL/RBAC; Databricks/Synapse roles; BI RLS | attribute-based policy, dynamic masking/tokenization |
| Network | private endpoints where budget/tenant permits | hub-spoke firewall, DNS, egress inspection |
| Audit | Azure activity, ADF, Databricks, Synapse, Power BI audit logs | central SIEM/SOC retention and alerting |

The project uses synthetic data and makes no claim of PCI DSS, GDPR, AML, or banking-regulator certification. GDPR-aware practices include minimisation, purpose limitation, access control, retention, traceability, and deletion design.
