-- ==============================================================================
-- Azure Synapse Analytics Dedicated SQL Pool: Dimension Tables DDL
-- Enterprise Star Schema with SCD Type 2 and Replicated Distributions
-- ==============================================================================

-- 1. Dim_Customer (SCD Type 2)
CREATE TABLE dbo.Dim_Customer (
    CustomerKey INT IDENTITY(1,1) NOT NULL,
    CustomerID VARCHAR(32) NOT NULL,
    FirstName NVARCHAR(100) NOT NULL,
    LastName NVARCHAR(100) NOT NULL,
    Email NVARCHAR(254) NULL,
    Phone NVARCHAR(32) NULL,
    KYCTier NVARCHAR(16) NOT NULL,
    CustomerStatus NVARCHAR(16) NOT NULL,
    Country CHAR(2) NOT NULL,
    ValidFrom DATETIME2 NOT NULL,
    ValidTo DATETIME2 NULL,
    IsCurrent BIT NOT NULL DEFAULT 1
)
WITH (
    DISTRIBUTION = REPLICATE,
    CLUSTERED COLUMNSTORE INDEX
);

-- 2. Dim_Account (SCD Type 1)
CREATE TABLE dbo.Dim_Account (
    AccountKey INT IDENTITY(1,1) NOT NULL,
    AccountID VARCHAR(32) NOT NULL,
    CustomerID VARCHAR(32) NOT NULL,
    AccountNumber VARCHAR(32) NOT NULL,
    AccountType NVARCHAR(32) NOT NULL,
    Currency CHAR(3) NOT NULL,
    AccountStatus NVARCHAR(16) NOT NULL,
    OpenedDate DATE NOT NULL,
    ClosedDate DATE NULL
)
WITH (
    DISTRIBUTION = REPLICATE,
    CLUSTERED COLUMNSTORE INDEX
);

-- 3. Dim_Merchant
CREATE TABLE dbo.Dim_Merchant (
    MerchantKey INT IDENTITY(1,1) NOT NULL,
    MerchantID VARCHAR(32) NOT NULL,
    MerchantName NVARCHAR(200) NOT NULL,
    Category NVARCHAR(64) NOT NULL,
    City NVARCHAR(100) NULL,
    Country CHAR(2) NOT NULL
)
WITH (
    DISTRIBUTION = REPLICATE,
    CLUSTERED COLUMNSTORE INDEX
);

-- 4. Dim_Card
CREATE TABLE dbo.Dim_Card (
    CardKey INT IDENTITY(1,1) NOT NULL,
    CardID VARCHAR(32) NOT NULL,
    CustomerID VARCHAR(32) NOT NULL,
    CardType NVARCHAR(16) NOT NULL,
    MaskedPan NVARCHAR(20) NOT NULL,
    CardStatus NVARCHAR(16) NOT NULL,
    IssuedDate DATE NOT NULL
)
WITH (
    DISTRIBUTION = REPLICATE,
    CLUSTERED COLUMNSTORE INDEX
);

-- 5. Dim_Date
CREATE TABLE dbo.Dim_Date (
    DateKey INT NOT NULL PRIMARY KEY NONCLUSTERED,
    FullDate DATE NOT NULL,
    DayOfWeek INT NOT NULL,
    DayName NVARCHAR(10) NOT NULL,
    DayOfMonth INT NOT NULL,
    MonthNumber INT NOT NULL,
    MonthName NVARCHAR(10) NOT NULL,
    CalendarQuarter INT NOT NULL,
    CalendarYear INT NOT NULL,
    IsWeekend BIT NOT NULL
)
WITH (
    DISTRIBUTION = REPLICATE,
    CLUSTERED COLUMNSTORE INDEX
);
