# ADR-001: Cloud Provider Selection

**Date:** 2026-09-01  
**Status:** Accepted  
**Deciders:** Solutions Architect, Tech Lead

---

## Context

An enterprise banking data platform for a mid-sized organization requires cloud infrastructure for data ingestion, transformation, analytics, and business intelligence. The organization is evaluating multiple cloud providers with different strengths and trade-offs.

## Decision

**Adopt Microsoft Azure as the primary cloud platform.**

### Rationale

1. **Integrated Data Platform:** ADLS Gen2 + Databricks + Synapse + ADF + Power BI work seamlessly together
2. **Databricks Co-Engineering:** Optimized performance and native managed identity integration
3. **Enterprise Identity:** Microsoft Entra ID provides advanced security features
4. **Cost Optimization:** Reserved instances, spot instances (70% discount), pause/resume capability
5. **Managed Services:** Reduces operational overhead

---

## Alternatives Considered

**AWS:** Market leader but requires more custom integration work; Databricks less tightly integrated  
**GCP:** BigQuery excellent for analytics but separate tool integrations required; less mature Entra ID equivalent

---

## Consequences

**Positive:**
- ✓ Simplified, integrated architecture
- ✓ Faster time-to-value
- ✓ Enterprise-grade security
- ✓ Clear cost visibility

**Negative:**
- ✗ Vendor lock-in
- ✗ Skills availability
- ✗ Feature gaps vs. competitors

---

**Related:** ADR-002, ADR-003, ADR-007
