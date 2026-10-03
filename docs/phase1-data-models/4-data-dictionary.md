# Core data dictionary

| Entity | Key | Important fields | Classification |
|---|---|---|---|
| customer | `customer_id` | name, email, phone, KYC tier | Confidential PII |
| account | `account_id` | customer id, type, currency, balance | Confidential financial |
| transaction | `transaction_id` | account id, time, amount, channel | Restricted financial |
| loan | `loan_id` | customer id, principal, rate, term | Restricted financial |
| repayment | `repayment_id` | loan id, amount, status | Restricted financial |
| card | `card_id` | customer id, masked PAN, status | Restricted PCI-adjacent |
| interaction/event | event id | customer/account id, event time, event type | Confidential behavioural |

Full PAN, CVV, passwords, and authentication secrets are prohibited from this platform.
