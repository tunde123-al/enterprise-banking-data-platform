-- Oracle Free : loans and repayments source schema.
-- Column names match the synthetic generator output (unquoted identifiers).
CREATE TABLE loans (
    loan_id          VARCHAR2(32) PRIMARY KEY,
    customer_id      VARCHAR2(32) NOT NULL,
    account_id       VARCHAR2(32),
    branch_id        VARCHAR2(32),
    loan_number      VARCHAR2(32),
    loan_type        VARCHAR2(32),
    principal_amount NUMBER(18, 2),
    interest_rate    NUMBER(5, 4),
    current_balance  NUMBER(18, 2),
    term_months      NUMBER(5),
    origination_date DATE,
    maturity_date    DATE,
    status           VARCHAR2(16),
    risk_rating      VARCHAR2(2),
    created_date     DATE,
    updated_date     DATE
);

CREATE TABLE repayments (
    repayment_id VARCHAR2(32) PRIMARY KEY,
    loan_id      VARCHAR2(32) NOT NULL REFERENCES loans (loan_id),
    payment_ts   TIMESTAMP,
    amount       NUMBER(18, 2),
    status       VARCHAR2(16)
);

CREATE INDEX ix_loans_customer ON loans (customer_id);
-- Oracle XE Legacy Banking System DDL
ALTER SESSION SET CURRENT_SCHEMA = bankadmin;

CREATE TABLE loans (
    loan_id VARCHAR2(32) PRIMARY KEY,
    customer_id VARCHAR2(32) NOT NULL,
    account_id VARCHAR2(32) NOT NULL,
    loan_type VARCHAR2(32) NOT NULL,
    principal_amount NUMBER(18,2) NOT NULL,
    interest_rate NUMBER(5,2) NOT NULL,
    term_months NUMBER(3) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    status VARCHAR2(16) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE repayments (
    repayment_id VARCHAR2(32) PRIMARY KEY,
    loan_id VARCHAR2(32) NOT NULL REFERENCES loans(loan_id),
    repayment_date DATE NOT NULL,
    amount NUMBER(18,2) NOT NULL,
    principal_component NUMBER(18,2) NOT NULL,
    interest_component NUMBER(18,2) NOT NULL,
    status VARCHAR2(16) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX ix_repayments_loan ON repayments(loan_id);
