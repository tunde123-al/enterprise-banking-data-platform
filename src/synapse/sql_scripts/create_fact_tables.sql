-- ==============================================================================
-- Azure Synapse Analytics Dedicated SQL Pool: Fact Tables DDL
-- Hash-Distributed Fact Tables with Clustered Columnstore Indexes
-- ==============================================================================

-- 1. Fact_Transactions (Core High-Volume Fact Table)
CREATE TABLE dbo.Fact_Transactions (
    TransactionKey BIGINT IDENTITY(1,1) NOT NULL,
    TransactionID VARCHAR(64) NOT NULL,
    TransactionReference VARCHAR(64) NOT NULL,
    AccountKey INT NOT NULL,
    MerchantKey INT NOT NULL,
    DateKey INT NOT NULL,
    TransactionDate DATETIME2 NOT NULL,
    TransactionType NVARCHAR(32) NOT NULL,
    TransactionCategory NVARCHAR(64) NOT NULL,
    Amount DECIMAL(18,2) NOT NULL,
    Fee DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    BalanceAfter DECIMAL(18,2) NOT NULL,
    TransactionStatus NVARCHAR(16) NOT NULL
)
WITH (
    DISTRIBUTION = HASH(AccountKey),
    CLUSTERED COLUMNSTORE INDEX,
    PARTITION (
        DateKey RANGE RIGHT FOR VALUES (
            20240101, 20240401, 20240701, 20241001,
            20250101, 20250401, 20250701, 20251001,
            20260101, 20260401, 20260701, 20261001
        )
    )
);

-- 2. Fact_Daily_Balances (Periodic Snapshot Fact Table)
CREATE TABLE dbo.Fact_Daily_Balances (
    DailyBalanceKey BIGINT IDENTITY(1,1) NOT NULL,
    AccountKey INT NOT NULL,
    DateKey INT NOT NULL,
    ClosingBalance DECIMAL(18,2) NOT NULL,
    TotalDeposits DECIMAL(18,2) NOT NULL,
    TotalWithdrawals DECIMAL(18,2) NOT NULL,
    TransactionCount INT NOT NULL
)
WITH (
    DISTRIBUTION = HASH(AccountKey),
    CLUSTERED COLUMNSTORE INDEX
);

-- 3. Fact_Loans (Accumulating Snapshot Fact Table)
CREATE TABLE dbo.Fact_Loans (
    LoanKey INT IDENTITY(1,1) NOT NULL,
    LoanID VARCHAR(32) NOT NULL,
    CustomerKey INT NOT NULL,
    AccountKey INT NOT NULL,
    LoanType NVARCHAR(32) NOT NULL,
    PrincipalAmount DECIMAL(18,2) NOT NULL,
    InterestRate DECIMAL(5,2) NOT NULL,
    TermMonths INT NOT NULL,
    OriginationDateKey INT NOT NULL,
    MaturityDateKey INT NOT NULL,
    LoanStatus NVARCHAR(16) NOT NULL,
    ProbabilityOfDefault DECIMAL(5,4) NOT NULL,
    ExpectedLoss DECIMAL(18,2) NOT NULL,
    CreditRating CHAR(3) NOT NULL
)
WITH (
    DISTRIBUTION = HASH(CustomerKey),
    CLUSTERED COLUMNSTORE INDEX
);

-- 4. Fact_Fraud_Alerts
CREATE TABLE dbo.Fact_Fraud_Alerts (
    AlertKey INT IDENTITY(1,1) NOT NULL,
    AlertID VARCHAR(64) NOT NULL,
    TransactionKey BIGINT NOT NULL,
    AccountKey INT NOT NULL,
    DateKey INT NOT NULL,
    FraudScore DECIMAL(4,2) NOT NULL,
    RiskBand NVARCHAR(16) NOT NULL,
    InvestigationStatus NVARCHAR(32) NOT NULL DEFAULT 'OPEN',
    FlaggedAt DATETIME2 NOT NULL
)
WITH (
    DISTRIBUTION = HASH(AccountKey),
    CLUSTERED COLUMNSTORE INDEX
);

-- 5. Fact_AML_Alerts
CREATE TABLE dbo.Fact_AML_Alerts (
    AMLAlertKey INT IDENTITY(1,1) NOT NULL,
    AMLAlertID VARCHAR(64) NOT NULL,
    AccountKey INT NOT NULL,
    DateKey INT NOT NULL,
    Amount DECIMAL(18,2) NOT NULL,
    RuleTriggered NVARCHAR(64) NOT NULL,
    RiskScore DECIMAL(4,2) NOT NULL,
    SARRecommended BIT NOT NULL,
    FlaggedAt DATETIME2 NOT NULL
)
WITH (
    DISTRIBUTION = ROUND_ROBIN,
    CLUSTERED COLUMNSTORE INDEX
);
