# Logical data model

| Entity | Primary/business key | Important relationships |
| --- | --- | --- |
| Customer | `customer_sk` / `customer_bk` | 1:M account, card, loan, device, interaction, AML alert |
| Account | `account_sk` / `account_number` | M:1 customer/branch; 1:M transaction/card |
| Transaction | `transaction_sk` / `transaction_id` | M:1 account, optional card/merchant; 1:M fraud event |
| Card | `card_sk` / `card_token` | M:1 customer/account |
| Merchant | `merchant_sk` / `merchant_id` | 1:M transaction |
| Loan | `loan_sk` / `loan_id` | M:1 customer; 1:M repayment |
| Repayment | `repayment_sk` / `repayment_id` | M:1 loan |
| Device | `device_sk` / `device_id` | M:1 customer |
| Customer interaction | `interaction_sk` / `interaction_id` | M:1 customer |
| AML alert | `aml_alert_sk` / `aml_alert_id` | M:1 customer; M:M transaction via evidence |
| Fraud event | `fraud_event_sk` / `fraud_event_id` | M:1 transaction |
| Branch | `branch_sk` / `branch_code` | 1:M account |

Facts retain event/business identifiers and dimension surrogate keys. `dim_customer` and `dim_branch` carry `effective_from`, `effective_to`, and `is_current` for SCD2 history. Transaction facts use date keys and are immutable except for documented reversal/status updates.
