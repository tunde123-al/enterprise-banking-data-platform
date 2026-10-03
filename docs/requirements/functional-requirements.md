# Functional requirements

| ID | Requirement | Priority |
| --- | --- | --- |
| FR-01 | Maintain synthetic customer, account, card, branch, and device records with stable business keys. | MVP |
| FR-02 | Ingest transactions, loans, repayments, interactions, and events with source/batch metadata. | MVP |
| FR-03 | Load relational extracts through ADF and document/event workflows through Airflow. | MVP |
| FR-04 | Validate schema, completeness, uniqueness, validity, referential integrity, freshness, and volume. | MVP |
| FR-05 | Quarantine invalid records and publish a quality result without silently dropping data. | MVP |
| FR-06 | Build conformed Customer, Account, Transaction, Loan, Merchant, and Branch Silver entities. | MVP |
| FR-07 | Produce fraud scores/rules, credit snapshots, AML candidates, Customer 360, and executive Gold datasets. | MVP |
| FR-08 | Maintain end-to-end source-to-BI lineage, run ID, code version, and data owner. | MVP |
| FR-09 | Build Power BI dashboards with role-appropriate views and refresh metadata. | MVP |
| FR-10 | Provide API simulation only for synthetic transaction/event generation; no payment execution. | Phase 2 |

### Use-case acceptance criteria

| Use case | Acceptance criterion |
| --- | --- |
| Fraud | analyst can filter flagged transactions, view rule/score evidence, and reconcile counts to Gold data |
| Credit | dashboard shows exposure, repayment and delinquency by branch/product with documented definitions |
| AML | candidate alerts retain linked customer, transactions, threshold/rule, and disposition placeholder |
| Customer 360 | authorised user finds a customer’s products, recent activity, interactions and risk flags by stable key |
| Executive | daily metrics reconcile to approved Gold aggregates and show refresh/quality timestamp |
