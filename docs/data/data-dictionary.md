# Data dictionary (initial)

| Dataset | Key fields | Selected attributes | Classification / owner |
| --- | --- | --- | --- |
| Customer | customer_bk, customer_sk | name (synthetic), DOB band, segment, status | confidential / Customer domain |
| Account | account_number, account_sk | product, currency, opened_at, status, balance | confidential / Core Banking |
| Transaction | transaction_id, transaction_sk | timestamp, amount, direction, channel, merchant | confidential / Payments |
| Card | card_token, card_sk | type, status, expiry month; no PAN/CVV | confidential / Cards |
| Merchant | merchant_id, merchant_sk | name, MCC, location | internal / Payments |
| Loan | loan_id, loan_sk | product, principal, rate, status, term | confidential / Lending |
| Repayment | repayment_id, repayment_sk | paid_at, amount, method | confidential / Lending |
| Device | device_id, device_sk | type, fingerprint token, first/last seen | confidential / Digital |
| Interaction | interaction_id, interaction_sk | channel, type, timestamp, outcome | confidential / Digital |
| AML alert | aml_alert_id, aml_alert_sk | rule, score, status, created_at | restricted / Compliance |
| Fraud event | fraud_event_id, fraud_event_sk | score, rule, disposition | restricted / Fraud |
| Branch | branch_code, branch_sk | name, region, status | internal / Branch operations |
