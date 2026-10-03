-- ==============================================================================
-- Azure Synapse Analytics: Reporting & BI Consumption Views
-- ==============================================================================

-- 1. Executive Banking KPI View
CREATE OR ALTER VIEW dbo.vw_executive_kpi_dashboard AS
SELECT 
    d.CalendarYear,
    d.MonthName,
    a.AccountType,
    c.Country,
    COUNT(DISTINCT t.TransactionKey) AS TotalTransactions,
    SUM(t.Amount) AS TotalTransactionVolume,
    AVG(t.Amount) AS AverageTicketSize,
    SUM(t.Fee) AS TotalFeeRevenue
FROM dbo.Fact_Transactions t
JOIN dbo.Dim_Date d ON t.DateKey = d.DateKey
JOIN dbo.Dim_Account a ON t.AccountKey = a.AccountKey
JOIN dbo.Dim_Customer c ON a.CustomerID = c.CustomerID AND c.IsCurrent = 1
GROUP BY d.CalendarYear, d.MonthName, a.AccountType, c.Country;
GO

-- 2. Customer 360 Analytical View
CREATE OR ALTER VIEW dbo.vw_customer_360 AS
SELECT 
    c.CustomerID,
    c.FirstName,
    c.LastName,
    c.Email,
    c.KYCTier,
    c.CustomerStatus,
    c.Country,
    COUNT(DISTINCT a.AccountKey) AS TotalActiveAccounts,
    ISNULL(SUM(b.ClosingBalance), 0) AS TotalDepositBalance,
    COUNT(DISTINCT cd.CardKey) AS TotalActiveCards,
    COUNT(DISTINCT l.LoanKey) AS TotalActiveLoans,
    ISNULL(SUM(l.PrincipalAmount), 0) AS TotalLoanLiabilities
FROM dbo.Dim_Customer c
LEFT JOIN dbo.Dim_Account a ON c.CustomerID = a.CustomerID AND a.AccountStatus = 'active'
LEFT JOIN dbo.Fact_Daily_Balances b ON a.AccountKey = b.AccountKey
LEFT JOIN dbo.Dim_Card cd ON c.CustomerID = cd.CustomerID AND cd.CardStatus = 'active'
LEFT JOIN dbo.Fact_Loans l ON c.CustomerKey = l.CustomerKey AND l.LoanStatus = 'active'
WHERE c.IsCurrent = 1
GROUP BY c.CustomerID, c.FirstName, c.LastName, c.Email, c.KYCTier, c.CustomerStatus, c.Country;
GO

-- 3. Fraud Risk Monitoring View
CREATE OR ALTER VIEW dbo.vw_fraud_risk_monitoring AS
SELECT 
    f.AlertID,
    f.FraudScore,
    f.RiskBand,
    f.InvestigationStatus,
    f.FlaggedAt,
    t.TransactionReference,
    t.Amount,
    t.TransactionType,
    a.AccountNumber,
    c.CustomerID,
    c.FirstName + ' ' + c.LastName AS CustomerFullName
FROM dbo.Fact_Fraud_Alerts f
JOIN dbo.Fact_Transactions t ON f.TransactionKey = t.TransactionKey
JOIN dbo.Dim_Account a ON f.AccountKey = a.AccountKey
JOIN dbo.Dim_Customer c ON a.CustomerID = c.CustomerID AND c.IsCurrent = 1;
GO

-- 4. Credit Portfolio Risk View
CREATE OR ALTER VIEW dbo.vw_credit_portfolio_risk AS
SELECT 
    l.LoanType,
    l.CreditRating,
    COUNT(l.LoanKey) AS TotalLoans,
    SUM(l.PrincipalAmount) AS TotalPrincipalExposure,
    AVG(l.InterestRate) AS WeightedAvgInterestRate,
    AVG(l.ProbabilityOfDefault) AS AvgProbabilityOfDefault,
    SUM(l.ExpectedLoss) AS PortfolioExpectedLoss
FROM dbo.Fact_Loans l
GROUP BY l.LoanType, l.CreditRating;
GO

-- 5. AML Compliance Investigation View
CREATE OR ALTER VIEW dbo.vw_aml_compliance_dashboard AS
SELECT 
    aml.AMLAlertID,
    aml.RuleTriggered,
    aml.RiskScore,
    aml.SARRecommended,
    aml.Amount,
    aml.FlaggedAt,
    a.AccountNumber,
    c.CustomerID,
    c.KYCTier,
    c.Country
FROM dbo.Fact_AML_Alerts aml
JOIN dbo.Dim_Account a ON aml.AccountKey = a.AccountKey
JOIN dbo.Dim_Customer c ON a.CustomerID = c.CustomerID AND c.IsCurrent = 1;
GO
