# DATA ARCHITECTURE
## Data Model, Ownership, Lifecycle & Governance

**Document Version:** 1.0  
**Date:** 2026-09-01  
**Audience:** Data Engineers, Solutions Architects, Data Stewards

---

## EXECUTIVE SUMMARY

The data architecture defines how enterprise banking data flows from operational sources through a Medallion Lake (Bronze/Silver/Gold) to an analytics warehouse and BI layers. Data is organized by domain (Customer, Account, Transaction, Loan, Fraud, Risk, AML, Branch, Product), with clear ownership, lifecycle management, and quality standards.

---

## MEDALLION ARCHITECTURE

### Zone Definitions

| Zone | Purpose | Format | Retention | Owner | Access |
|------|---------|--------|-----------|-------|--------|
| **Bronze** | Raw, immutable data as-received | Parquet | 2 years | Data Eng | Dev/Test only |
| **Silver** | Cleaned, deduplicated, validated | Delta Lake | 2-5 years | Data Eng + Stewards | Analysts, Engineers |
| **Gold** | Business-aligned, aggregated analytics | Delta Lake | 5+ years | Domain Owners | All authorized users |
| **Warehouse** | Star schema, consumption-optimized SQL | Synapse tables | 5+ years | BI Team | BI & Power BI |

### Bronze Zone (2-Year Retention)

**Purpose:** Preserve original data exactly as received  
**Characteristics:**
- Data lands unchanged from source systems
- Full audit trail (source metadata, landing time, file size)
- Replay-able (can re-process if transformation fails)
- Immutable files (cannot be modified)
- Partitioned by source_date for efficient querying

**Structure:**
```
/bronze/{source_system}/{entity}/{year}/{month}/{day}/
Example:
  /bronze/postgresql/customers/2024/09/01/data.parquet
  /bronze/oracle/gl_ledger/2024/09/01/data.parquet
  /bronze/cassandra/events/2024/09/01/data.parquet
```

**Quality Checks Applied:**
- ✓ Schema validation (expected columns)
- ✓ Row count reconciliation vs. source
- ✓ File integrity (no corrupted records)
- ✓ Date range validation (no future data)

**Who Can Access:** Data Engineers only (transformation development)

---

### Silver Zone (2-5 Year Retention)

**Purpose:** Conformed, high-quality datasets for analytics  
**Format:** Delta Lake (ACID, time travel, schema enforcement)

**Transformations Applied:**
- ✓ Deduplication (remove business-key duplicates)
- ✓ Standardization (dates, formatting, units)
- ✓ Type validation (enforce correct data types)
- ✓ Null handling (apply business rules)
- ✓ Referential integrity checks (validate FK)
- ✓ Quarantine (failed records isolated, not lost)

**Quality Certification:**
- ✓ Schema matches business specifications
- ✓ Row count matches source ±0.1% (accounting for duplicates)
- ✓ Null percentage < defined thresholds
- ✓ Duplicate count = 0 or documented
- ✓ All dates within valid range

**Retention by Domain:**
- Customer, Account, Transaction, Card, Device: 2 years
- Loan, Repayment, Interaction: 2-5 years
- Branch, Merchant: Permanent (slowly changing reference data)

**Who Can Access:** Data Engineers + Analysts (validated data only)

---

### Gold Zone (5+ Year Retention)

**Purpose:** Business-aligned datasets optimized for consumption  
**Contents:**
- Business-level fact tables (transactions, events, scores)
- Slowly Changing Dimension tables (SCD Type 2)
- Pre-aggregated metrics (daily/monthly summaries)
- Feature-engineered datasets (risk scores, fraud indicators)

**Structure:**
```
/gold/
  /fact/ → Transactional facts (daily)
    /transactions/
    /fraud_scores/
    /credit_scores/
    /aml_alerts/
  /dimension/ → Reference data (SCD Type 2)
    /customers_scd2/
    /accounts_scd2/
    /merchants_scd2/
    /time/ (calendar dimension)
  /metrics/ → Pre-aggregated (daily)
    /daily_transaction_summary/
    /customer_segment_metrics/
    /portfolio_risk_daily/
```

**Who Can Access:** All authorized users (business-ready data)

---

## DATA DOMAINS & OWNERSHIP

### Domain 1: Customer Management (CRM)

| Aspect | Details |
|--------|---------|
| **Owner** | CRM Team / Customer Analytics |
| **Priority** | P1 (Critical) |
| **SLA** | 99% data freshness |
| **Bronze Source** | PostgreSQL, Azure SQL |
| **Key Entity** | Customer (500K-1M records) |

**Silver Table: customer**
- Primary key: `customer_key` (surrogate)
- Business key: `customer_id + country_code`
- Quality rule: 99.5% non-null email
- Deduplication: By customer_id

**Gold Tables:**
- `dim_customer_scd2` (historical changes tracked)
- `customer_segment` (lifetime value, lifecycle stage, risk tier)

**Data Lineage:**
```
PostgreSQL::customer_master
  ↓ (ADF Extract)
Bronze::customer
  ↓ (Databricks: dedupe, standardize)
Silver::customer
  ↓ (dbt: SCD2, segmentation)
Gold::dim_customer_scd2, Gold::customer_segment
  ↓ (Synapse materialize)
Warehouse::dim_customers
  ↓ (Power BI load)
BI Dashboard: Customer 360
```

---

### Domain 2: Transaction Processing (Finance)

| Aspect | Details |
|--------|---------|
| **Owner** | Operations / Finance |
| **Priority** | P0 (Critical Path) |
| **SLA** | 99.9% pipeline SLA |
| **Bronze Source** | PostgreSQL, Cassandra |
| **Volume** | 100K-500K tx/hour = 2.4B-12B/year |

**Silver Table: transaction**
- Primary key: `transaction_key` (surrogate)
- Business key: `transaction_id`
- Deduplication: By transaction_id (remove exact duplicates)
- Quality: 0% null in key columns, 100% valid merchant_id

**Gold Tables:**
- `fact_transaction_daily` (aggregated by day, merchant, customer)
- `fact_fraud_score` (real-time fraud indicators)
- `fact_credit_score` (credit risk by transaction)

**Data Quality Rules:**
- ✓ Amount > 0
- ✓ Transaction date <= current date
- ✓ Merchant ID exists in dim_merchant
- ✓ Customer ID exists in dim_customer
- ✓ Currency code in ISO-4217 list

---

### Domain 3: Loan & Credit (Risk Management)

| Aspect | Details |
|--------|---------|
| **Owner** | Credit Risk / Lending |
| **Priority** | P1 (Critical) |
| **SLA** | 99% data freshness |
| **Bronze Source** | SQL Server (lending system) |
| **Key Entities** | Loan (1M), Repayment (10M) |

**Silver Tables:**
- `loan` (deduplicated, validated)
- `repayment` (matched to loans, reconciled)

**Gold Tables:**
- `dim_loan_scd2` (status changes tracked: active → delinquent → defaulted)
- `fact_repayment_daily` (daily repayment summary)
- `credit_risk_score` (risk score per loan)

**Data Quality Rules:**
- ✓ Loan amount > 0
- ✓ Interest rate between 0-20%
- ✓ Repayment date >= loan origination date
- ✓ Outstanding balance = principal - total paid
- ✓ Next payment date > last payment date

**SCD Type 2 Tracking:**
- Loan status changes (approved → active → delinquent → charged-off)
- Interest rate changes (fixed rate changes, variable resets)
- Payment schedule modifications

---

### Domain 4: Fraud Detection (Risk)

| Aspect | Details |
|--------|---------|
| **Owner** | Fraud Team / Risk |
| **Priority** | P0 (Critical Path) |
| **SLA** | Real-time alerts |
| **Bronze Source** | Transaction, historical fraud labels |

**Features Engineered:**
- Amount anomaly (vs. customer average ±2 std dev)
- Frequency anomaly (vs. customer baseline)
- Geographic anomaly (unusual country)
- Merchant category anomaly
- Time-of-day anomaly (unusual hour)
- Velocity features (transactions in short time window)

**Gold Tables:**
- `fact_fraud_daily` (daily fraud by type, amount, customer)
- `fraud_risk_score` (0-100 score per transaction)
- `fraud_pattern_detection` (ring analysis, money mule detection)

**Alert Rules:**
- High-risk transactions: Score > 80
- Unusual account activity: > 10 transactions in 1 hour
- Cross-account patterns: Same merchant, multiple accounts, short timeframe
- Velocity rules: Multiple countries within 4 hours

---

### Domain 5: AML Compliance (Compliance)

| Aspect | Details |
|--------|---------|
| **Owner** | Compliance / Risk |
| **Priority** | P0 (Regulatory) |
| **SLA** | Real-time alerts |
| **Bronze Source** | Transaction, customer KYC, sanctions list |

**Compliance Rules:**
- ✓ Structured transactions (deposits just below $10K threshold)
- ✓ Rapid transfers (quick in/out patterns)
- ✓ PEP transactions (politically exposed persons)
- ✓ Sanctions matching (OFAC, UNSC lists)
- ✓ Customer baseline anomaly (unusual activity)
- ✓ Trade-based money laundering patterns

**Gold Tables:**
- `fact_aml_alert_daily` (suspicious activity alerts)
- `sar_case_log` (Suspicious Activity Report cases)
- `customer_risk_profile` (customer-level AML risk)

**Lineage & Audit Trail:**
- Every alert includes: rule triggered, threshold, transaction details, customer context
- SAR generation documented and tracked
- Investigation status logged

---

## DATA RETENTION POLICIES

### Retention Schedule

**Bronze Zone (2-Year Minimum):**
- Customer, Account, Transaction: 2 years
- Cassandra events: 1 year (high volume)
- Purpose: Audit trail, fraud investigation replay

**Silver Zone (2-5 Year Minimum):**
- Customer, Account, Transaction, Device: 2 years
- Loan, Repayment: 5 years (regulatory requirement)
- Purpose: Historical analysis, trend reporting

**Gold Zone (5+ Year Minimum):**
- All fact tables: 5 years (business requirement)
- All dimensions: Permanent (slowly changing reference)
- Purpose: Long-term trends, forecast modeling

**Warehouse (5+ Year Minimum):**
- Star schema: 5 years (aligned with Gold)
- Archive: Move to Cool tier after 1 year, Archive tier after 3 years

### Lifecycle Actions (Automated)

```
Day 0-30: Hot tier (immediate access)
  ├─ Active ingestion and transformation
  ├─ Full query performance
  └─ Used by: Analysts, dashboards

Day 31-365: Cool tier (infrequent access)
  ├─ Full data available but slower queries
  ├─ Lower storage cost
  └─ Used by: Historical analysis, audit

Day 366-1095: Archive tier (regulatory hold)
  ├─ Data retrievable but slow (hours)
  ├─ Minimal cost
  └─ Used by: Compliance, legal holds

Day 1095+: Delete (per policy)
  ├─ Post-retention deletion
  ├─ Compliance approval required
  └─ Audit trail maintained of deletion
```

---

## DATA QUALITY FRAMEWORK

### Quality Dimensions (6-Pillar Model)

| Dimension | Definition | Target | Check Frequency |
|-----------|---|---|---|
| **Completeness** | % non-null in key columns | 99.5% | Daily |
| **Accuracy** | % values correct vs. source | 99% | Daily |
| **Consistency** | Cross-domain matching (FK integrity) | 99.5% | Daily |
| **Uniqueness** | % business-key duplicates | 0% | Daily |
| **Timeliness** | Data freshness (age <= 24h) | 99% | Real-time |
| **Validity** | Values in valid domain | 99.5% | Daily |

### Quality Checks by Stage

**Bronze → Silver:**
- Schema validation: All expected columns present
- Row count: Match source ±10% (expected variance)
- Parse success: 100% records parseable (no truncation)
- Date range: No future dates, minimum year 1900
- Null percentage: Document baseline

**Silver → Gold:**
- Deduplication: Input rows ≥ output rows (expected effect)
- Referential integrity: 99.5% of FK match to dimension
- Type casting: 100% successful or quarantined
- Business rules: All domain validations pass
- Reconciliation: Aggregate sums match source

**Gold → Warehouse:**
- Fact count: Consistent day-over-day (±20% acceptable)
- Dimension completeness: All FK resolved
- Metric calculations: No NaN, Inf, or NULL results
- SCD Type 2: Effective dates don't overlap
- Freshness: Data <= 24 hours old

### Quarantine & Escalation

**Failed Records:**
- Isolated to `quarantine/` containers (not deleted)
- Tagged with failure reason and rule
- Investigated by Data Engineering
- Escalated if > 5% of records fail

**Pipeline Monitoring:**
- Automated alerts on quality metric deviations
- Email to data steward on failures
- PagerDuty alert if SLA at risk
- Weekly quality report to stakeholders

---

## DATA PRIVACY & SECURITY

### Data Classification

| Level | Examples | Encryption | Access Restriction |
|-------|----------|-----------|---|
| **Public** | Merchant name, transaction amount (anonymized) | Optional | All users |
| **Internal** | Customer counts, aggregate metrics | Recommended | Internal only |
| **Sensitive** | Customer name, email, phone | Required | Role-based |
| **Confidential** | Account balances, SSN, fraud labels | Required | Restricted |
| **Restricted** | Compliance data, SAR cases, legal holds | Required | Legal/Compliance only |

### Access Control

**By Zone:**
- **Bronze:** Data Engineers only (transformation maintenance)
- **Silver:** Data Engineers + Domain Stewards (validated data)
- **Gold:** Authorized users per domain (business-ready)

**By Role (Entra ID Groups):**
- DataEngineers: All zones (full access)
- FraudAnalysts: Gold/fraud tables + Synapse + Power BI
- ComplianceOfficers: Gold/AML tables + Synapse
- Analysts: Gold layer only (restricted rows)
- Executives: Aggregated/summarized views only

**Row-Level Security:**
- Fraud analysts: See transactions for assigned accounts only
- Compliance: See transactions for assigned customers only
- Product managers: See segment/cohort data only (no individual customers)
- Executives: Aggregated dashboards only (no individual-level detail)

---

## DATA DICTIONARY HIGHLIGHTS

### silver.customer

| Column | Type | Null% | Unique | Description |
|--------|------|-------|--------|---|
| customer_key | BIGINT | 0% | 100% | Surrogate key |
| customer_id | INT | 0% | 99.9% | Natural key from source |
| first_name | VARCHAR | 0% | N | Standardized, trimmed |
| email | VARCHAR | 0.5% | 99.8% | Validated format |
| country_code | VARCHAR(2) | 0% | 50 | ISO-3166 standard |
| status | VARCHAR | 0% | 3 | ACTIVE, CLOSED, DORMANT |

### gold.fact_transaction_daily

| Column | Type | Null% | Description |
|--------|------|-------|---|
| transaction_key | BIGINT | 0% | Surrogate key |
| customer_key | BIGINT | 0% | FK to dim_customer |
| account_key | BIGINT | 0% | FK to dim_account |
| transaction_date | DATE | 0% | Business date |
| amount | DECIMAL(15,2) | 0% | Transaction amount |
| fraud_risk_score | INT | 2% | 0-100 fraud likelihood |
| aml_alert_flag | BOOLEAN | 0% | AML alert triggered? |

---

## DATA LINEAGE DOCUMENTATION

All data lineage is tracked via dbt manifest + Azure Data Factory logs + Databricks notebooks.

**Master Lineage Reference:** See [data-lineage.md](data-lineage.md)

---

**Date:** 2026-09-01  
**Status:** Ready for Review  
**Next:** [Logical Architecture](3-logical-architecture.md)
