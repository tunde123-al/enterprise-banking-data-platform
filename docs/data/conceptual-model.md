# Conceptual data model

```mermaid
erDiagram
  CUSTOMER ||--o{ ACCOUNT : owns
  CUSTOMER ||--o{ CARD : holds
  ACCOUNT ||--o{ TRANSACTION : posts
  CARD ||--o{ TRANSACTION : initiates
  MERCHANT ||--o{ TRANSACTION : accepts
  CUSTOMER ||--o{ LOAN : borrows
  LOAN ||--o{ REPAYMENT : receives
  CUSTOMER ||--o{ DEVICE : uses
  CUSTOMER ||--o{ CUSTOMER_INTERACTION : has
  BRANCH ||--o{ ACCOUNT : services
  TRANSACTION ||--o{ FRAUD_EVENT : may_trigger
  CUSTOMER ||--o{ AML_ALERT : subject_of
```

Customer is the party master. Accounts hold balances and post transactions. Cards instrument account payments; merchants receive them. Loans and repayments model credit. Devices/interactions contribute digital context. Fraud events relate to transactions; AML alerts relate to customers and may cite many transactions through an alert-evidence bridge in the physical model.
