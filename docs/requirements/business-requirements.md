# BUSINESS REQUIREMENTS SPECIFICATION
## Enterprise Banking Data & Analytics Platform

**Document Version:** 1.0  
**Date:** 2026-09-01  
**Audience:** Business Stakeholders, Project Sponsors

---

## 1. EXECUTIVE SUMMARY

The Enterprise Banking Data & Analytics Platform consolidates data from 6 banking source systems to enable 5 critical business use cases: Fraud Detection, Credit Risk Management, AML Compliance, Customer 360 Analytics, and Executive KPI Reporting.

**MVP Scope:** Synthetic data for proof of concept  
**Timeline:** 3-4 months  
**Investment:** $550-650/month cloud infrastructure

---

## 2. BUSINESS PROBLEM

**Current State:**
- Fraud detection misses 10-15% of cases ($500K-1M annual loss)
- Credit risk assessed manually on quarterly basis
- AML monitoring lacks real-time capability
- Reports take days to generate manually
- No unified customer view

**Impact:** Regulatory risk, operational inefficiency, reduced revenue opportunity

---

## 3. BUSINESS OBJECTIVES

### Primary Objectives (MVP)

1. **Fraud Detection (80% accuracy target)**
   - Real-time transaction scoring
   - Cross-account fraud ring detection
   - Reduce false positives by 30%

2. **Credit Risk Management (Quarterly reporting)**
   - Portfolio risk distribution dashboards
   - Early warning indicators for defaults
   - Customer credit score trending

3. **AML Compliance (Real-time alerts)**
   - Transaction pattern monitoring
   - Customer behavior anomalies
   - Escalation to compliance team

4. **Customer 360 (Self-service analytics)**
   - Unified customer view across products
   - Customer segmentation
   - Cross-sell/up-sell analytics

5. **Executive Reporting (Daily KPIs)**
   - Transaction volume and trends
   - Revenue by product/segment
   - Risk metrics and exposure

---

## 4. PROJECT SCOPE

### Data Sources (6 systems)
- PostgreSQL: Core Banking (100K tx/hour)
- Oracle: Legacy System (5M records daily)
- SQL Server: Lending (2M records daily)
- Azure SQL: Cloud Apps (1M records real-time)
- MongoDB: Interactions (50M documents daily)
- Cassandra: Events (100M events/day)

### Use Cases (5 core)
✓ Fraud Detection Dashboard  
✓ Credit Risk Portfolio View  
✓ AML Transaction Monitoring  
✓ Customer 360 Analytics  
✓ Executive Daily KPIs

### MVP Capabilities
- ✓ Ingest 6 data sources daily
- ✓ Validate and clean data
- ✓ Load analytical data warehouse
- ✓ Create 5 executive dashboards
- ✓ Monitor data quality and pipeline health
- ✓ Document data lineage

---

## 5. STAKEHOLDERS

| Role | Responsibility | Count |
|------|---|---|
| Fraud Analyst | Dashboard monitoring, investigation | 3-5 |
| Credit Risk Manager | Risk reporting, portfolio monitoring | 2-3 |
| Compliance Officer | AML monitoring, regulatory reporting | 2-3 |
| Product Manager | Customer analytics, segmentation | 2-3 |
| Executive | Strategic KPI review | 3-5 |

---

## 6. BUSINESS REQUIREMENTS BY USE CASE

### Use Case 1: Fraud Detection
- Real-time transaction scoring (< 100ms)
- Detect account takeover and money mule rings
- 80% accuracy, < 5% false positives
- Daily fraud metrics and trending

### Use Case 2: Credit Risk
- Portfolio risk distribution
- Customer risk scoring (0-100)
- Alert on score changes > 10 points
- Product-level risk analysis

### Use Case 3: AML Monitoring
- Structured transaction detection
- Rapid transfer identification
- PEP transaction flagging
- SAR (Suspicious Activity Report) generation

### Use Case 4: Customer 360
- Unified customer view across products
- Customer segmentation (behavioral, lifecycle)
- Lifetime value by segment
- Churn risk identification

### Use Case 5: Executive Analytics
- Daily KPI dashboard (revenue, volume, risk, operations)
- Business performance metrics
- Trend analysis and comparisons
- Alert management

---

## 7. CONSTRAINTS & ASSUMPTIONS

### Constraints
- Banking Secrecy Act (BSA) compliance required
- Encryption required for data at rest and in transit
- Annual compliance audits
- Budget: < $50K annually (MVP)
- Timeline: 3-4 months MVP delivery

### Assumptions
- Source systems provide valid, clean data
- Historical data available for 2+ years
- Team has Python/SQL expertise
- Synthetic data sufficient for MVP (not real customer data)
- Batch processing acceptable (not real-time streaming)

---

## 8. ACCEPTANCE CRITERIA (MVP Go/No-Go)

- ✓ All 6 source systems successfully integrated
- ✓ Daily pipeline executes in < 6 hours
- ✓ Data quality metrics > 99% pass rate
- ✓ 5 executive dashboards deployed and validated
- ✓ Fraud detection 80%+ accuracy
- ✓ AML alerts operational
- ✓ Security audit passed
- ✓ Backup and recovery tested

---

## 9. SUCCESS METRICS

| Metric | Baseline | Target | Owner |
|--------|----------|--------|-------|
| Fraud detection accuracy | 60% | 80% | Fraud Team |
| False positive rate | 15% | < 5% | Fraud Team |
| AML alert response time | 24h | 1h | Compliance |
| Report generation time | 2 days | < 2h | BI Team |
| Pipeline SLA | N/A | 99% | Eng Team |
| Customer 360 completeness | 80% | 95% | Product |

---

**Status:** Draft - Ready for Business Review

**In scope:** synthetic source integration; batch lakehouse ingestion; Bronze/Silver/Gold data products; Synapse/dbt marts; dashboards; monitoring; access controls; documented lineage. **Out of scope:** real customer data, payment authorisation, regulatory filing, automated adverse decisions, real-time fraud blocking, and regulatory certification.

| Stakeholder/persona | Need |
| --- | --- |
| Executive sponsor | trusted trend and portfolio KPIs |
| Fraud/AML analyst | explainable alert candidates and transaction evidence |
| Credit analyst | exposure, repayment, delinquency views |
| Relationship manager | governed Customer 360 view |
| Data engineer | repeatable pipelines, quality results, reruns |
| Data steward/auditor | ownership, classification, lineage and access evidence |

## Business requirements

| ID | Requirement | Release |
| --- | --- | --- |
| BR-01 | Consolidate named source domains using repeatable, auditable ingestion. | MVP |
| BR-02 | Publish five governed Gold products with definitions and owners. | MVP |
| BR-03 | Preserve source-to-report lineage and quality status. | MVP |
| BR-04 | Restrict confidential synthetic data by role and expose aggregate BI views. | MVP |
| BR-05 | Support near-real-time event micro-batching after batch foundation succeeds. | Phase 2 |
| BR-06 | Add ML model lifecycle/governance before predictive decisions. | Production extension |

## Reporting and analytics requirements

Dashboards: Fraud Operations, Credit Portfolio, AML Monitoring, Customer 360, and Executive Banking Overview. Each must state source refresh time, filters, metric definition, and quality status. Certified Power BI models use a star schema and DAX for standard measures. Python may perform offline segmentation, distribution/anomaly analysis, or an approved visual; it must not be the sole definition of an executive KPI and is constrained by Power BI refresh/runtime limitations.

## Assumptions, constraints, approvals needed

Assumptions: one Azure region; synthetic data; daily batch baseline; a private repository; source simulators are available; no externally managed production SLA. Constraints: personal Azure budget, limited service quotas, no real compliance attestation, and source systems may be containerised/emulated.

Approval decisions: (1) choose Terraform *or* ARM as the authoritative IaC path; (2) confirm Azure region and budget ceiling; (3) decide whether Oracle/SQL Server/Cassandra run locally or are schema-only simulations; (4) select Power BI licence/capacity; (5) approve daily batch MVP and defer streaming; (6) approve which role receives customer-level masked fields.

## Risks and mitigation

| Risk | Mitigation |
| --- | --- |
| unnecessary technology sprawl | responsibility matrix and MVP service selection |
| cloud cost overrun | auto-termination, serverless where suitable, pause/delete idle capacity, budgets/tags |
| poor synthetic quality | seeded generation, contracts, reconciliation and quality tests |
| duplicate orchestration | ADF owns relational movement; Airflow owns code/event demonstration workflows |
| sensitive data mistake | synthetic-only guardrail, Git secret scanning, Key Vault, no `.env` commit |
