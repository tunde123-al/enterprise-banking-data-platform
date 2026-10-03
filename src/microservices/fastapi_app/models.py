from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str
    app: str
    environment: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class TransactionCreateRequest(BaseModel):
    account_id: str
    amount: float = Field(gt=0, description="Transaction amount must be positive")
    currency: str = "USD"
    transaction_type: str = Field(description="deposit, withdrawal, transfer, payment, fee")
    transaction_category: str = "general"
    merchant_id: Optional[str] = None
    channel: str = "online"
    description: Optional[str] = None


class TransactionResponse(BaseModel):
    transaction_id: str
    account_id: str
    transaction_reference: str
    amount: float
    currency: str
    transaction_type: str
    status: str
    balance_after: float
    timestamp: datetime


class AccountBalanceResponse(BaseModel):
    account_id: str
    customer_id: str
    account_type: str
    balance: float
    available_balance: float
    currency: str
    status: str


class AMLAlertEvent(BaseModel):
    alert_id: str
    account_id: str
    transaction_id: str
    amount: float
    reason: str
    risk_level: str
    flagged_at: datetime = Field(default_factory=datetime.utcnow)
