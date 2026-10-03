-- PostgreSQL Core Banking Schema Initialization
CREATE SCHEMA IF NOT EXISTS core_banking;

CREATE TABLE IF NOT EXISTS core_banking.customers (
    customer_id VARCHAR(32) PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(254),
    phone VARCHAR(32),
    date_of_birth DATE,
    ssn_hash CHAR(64),
    address VARCHAR(200),
    city VARCHAR(100),
    state CHAR(2),
    zip VARCHAR(16),
    country CHAR(3),
    kyc_tier VARCHAR(16),
    created_date DATE,
    updated_date DATE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS core_banking.accounts (
    account_id VARCHAR(32) PRIMARY KEY,
    customer_id VARCHAR(32) NOT NULL REFERENCES core_banking.customers(customer_id),
    branch_code VARCHAR(16),
    account_number VARCHAR(32),
    account_type VARCHAR(32) NOT NULL,
    currency CHAR(3) NOT NULL DEFAULT 'USD',
    balance NUMERIC(18,2) NOT NULL DEFAULT 0.00,
    available_balance NUMERIC(18,2),
    opened_date DATE NOT NULL,
    closed_date DATE,
    status VARCHAR(16) NOT NULL,
    created_date DATE,
    updated_date DATE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS core_banking.merchants (
    merchant_id VARCHAR(32) PRIMARY KEY,
    merchant_name VARCHAR(200) NOT NULL,
    merchant_code VARCHAR(16),
    category_code VARCHAR(8),
    category_name VARCHAR(100) NOT NULL,
    address VARCHAR(200),
    city VARCHAR(100),
    state CHAR(2),
    country CHAR(3) NOT NULL,
    created_date DATE
);

CREATE TABLE IF NOT EXISTS core_banking.transactions (
    transaction_id VARCHAR(64) PRIMARY KEY,
    account_id VARCHAR(32) NOT NULL REFERENCES core_banking.accounts(account_id),
    merchant_id VARCHAR(32) REFERENCES core_banking.merchants(merchant_id),
    transaction_reference VARCHAR(64) NOT NULL,
    amount NUMERIC(18,2) NOT NULL,
    currency CHAR(3) NOT NULL DEFAULT 'USD',
    transaction_type VARCHAR(32) NOT NULL,
    transaction_category VARCHAR(64) NOT NULL,
    transaction_date TIMESTAMPTZ NOT NULL,
    balance_after NUMERIC(18,2) NOT NULL,
    status VARCHAR(16) NOT NULL,
    description TEXT,
    fee NUMERIC(10,2) DEFAULT 0.00,
    tax NUMERIC(10,2) DEFAULT 0.00,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS ix_transactions_account_date ON core_banking.transactions(account_id, transaction_date);
CREATE INDEX IF NOT EXISTS ix_transactions_type ON core_banking.transactions(transaction_type);
CREATE INDEX IF NOT EXISTS ix_accounts_customer ON core_banking.accounts(customer_id);
