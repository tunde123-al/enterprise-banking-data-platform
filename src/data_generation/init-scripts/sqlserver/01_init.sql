-- SQL Server Loan & Branch System DDL
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'loan_management')
BEGIN
    CREATE DATABASE loan_management;
END
GO

USE loan_management;
GO

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'cards')
BEGIN
    CREATE TABLE dbo.cards (
        card_id VARCHAR(32) PRIMARY KEY,
        customer_id VARCHAR(32) NOT NULL,
        card_number_masked VARCHAR(20) NOT NULL,
        card_type VARCHAR(16) NOT NULL,
        expiry_date VARCHAR(10) NOT NULL,
        cvv_hash VARCHAR(64) NOT NULL,
        status VARCHAR(16) NOT NULL,
        issued_date DATE NOT NULL,
        created_at DATETIME2 DEFAULT CURRENT_TIMESTAMP
    );
END
GO

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'devices')
BEGIN
    CREATE TABLE dbo.devices (
        device_id VARCHAR(32) PRIMARY KEY,
        customer_id VARCHAR(32) NOT NULL,
        device_type VARCHAR(32) NOT NULL,
        os VARCHAR(32) NOT NULL,
        browser VARCHAR(32) NOT NULL,
        ip_address VARCHAR(45) NOT NULL,
        is_trusted BIT DEFAULT 1,
        last_login DATETIME2 NOT NULL,
        created_at DATETIME2 DEFAULT CURRENT_TIMESTAMP
    );
END
GO
