# Power BI Semantic Model & Analytical Architecture

## Overview
This directory defines the Power BI semantic modeling layer for the Enterprise Banking Data & Analytics Platform. It connects directly to the curated **Gold Delta Lake** tables and **Azure Synapse Analytics Dedicated SQL Pool** marts.

## Repository layout

| Path | Purpose |
| --- | --- |
| `dax/measures.dax` | Certified DAX measures for all five use-case dashboards |
| `row_level_security.dax` | RLS roles (branch/country, AML officer, executive) with test personas |
| `scripts/python_powerbi_segmentation.py` | Python visual: K-Means customer wealth & activity segmentation |
| `scripts/python_powerbi_anomaly_detection.py` | Python visual: robust z-score outlier detection on transaction amounts |
| `README.md` | Semantic model, star schema, refresh and Python-usage guidance |

## Architecture & Data Model
- **Storage Mode**: Dual / DirectQuery for Real-Time Transaction facts, Import mode for Dimension tables and aggregated Marts.
- **Model** (Synapse marts):
  - Executive: `mart_executive_kpis`
  - Fraud: `mart_fraud_monitoring`
  - AML: `mart_aml_monitoring`
  - Credit: `mart_credit_risk`
  - Customer 360: `mart_customer_360`
- **Facts** (SQL pool): `Fact_Transactions`, `Fact_Daily_Balances`, `Fact_Loans`, `Fact_Fraud_Alerts`, `Fact_AML_Alerts`
- **Dimensions** (SQL pool): `Dim_Customer` (SCD2), `Dim_Account`, `Dim_Card`, `Dim_Merchant`, `Dim_Branch`, `Dim_Date`, `Dim_Device`

## Row-Level Security (RLS)
Implemented in `row_level_security.dax` using a `UserSecurity` mapping table and `USERPRINCIPALNAME()`:
1. **Branch / Country RLS** - branch managers see only their geography.
2. **AML Officer Role** - unrestricted access to `Fact_AML_Alerts` / `Fact_Fraud_Alerts`.
3. **Retail Banking Executive Role** - aggregated KPIs without SSN or unmasked PII.

## Python inside Power BI
Power BI allows embedded Python execution for advanced statistical visuals and ad-hoc exploration:
- `python_powerbi_segmentation.py` - customer segmentation with scikit-learn K-Means.
- `python_powerbi_anomaly_detection.py` - MAD-based robust z-score anomaly chart.

**When to use Python in Power BI**
- Statistically demanding exploration (clustering, robust anomaly detection, bespoke chart types).
- Prototype analysis where a DAX formula would be convoluted or unreadable.

**Limitations & when to prefer DAX / standard visuals**
- Python visuals are static images: they do not cross-filter with other visuals and cannot be used in tooltips, drill-through, or live summary cards.
- Python execution is per-visual, per-refresh and can be slow on desktop-scale datasets; never push large raw tables through Python.
- Governed KPIs that enter certification should always be DAX (testable, lineage-tracked, refresh-optimised).
- Recommended Data-hub rule: Python for exploration; DAX + native visuals for certified dashboards.

## Refresh strategy
- **Import tables** (dims, marts): daily incremental refresh after the dbt `build` completes (Synapse marts).
- **Real-time facts**: DirectQuery to Synapse views (`vw_executive_kpi_dashboard`, `vw_customer_360`, `vw_fraud_risk_monitoring`, `vw_credit_portfolio_risk`, `vw_aml_compliance_dashboard`) with constrained direct query caching.
- Refresh is triggered from Airflow after the dbt step (task `notify_pipeline_success`) or scheduled in the Power BI Service (production extension).

## Getting started
1. Load Gold / Synapse marts (run the dbt project in `src/dbt`).
2. Create the model in Power BI Desktop pointing at the marts/views above.
3. Import `dax/measures.dax` measures, apply `row_level_security.dax` roles.
4. Add Python visuals from `scripts/` where exploration value justifies them.
