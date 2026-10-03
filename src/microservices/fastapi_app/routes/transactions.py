import uuid
from datetime import datetime
from fastapi import APIRouter, HTTPException, status
from ..models import TransactionCreateRequest, TransactionResponse

router = APIRouter(prefix="/transactions", tags=["Transactions"])

# In-memory mock balances for operational simulation
_MOCK_BALANCES = {
    "ACC00000001": 15420.50,
    "ACC00000002": 2840.10,
    "ACC00000003": 95300.00,
}


@router.post("/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def create_transaction(txn: TransactionCreateRequest):
    current_balance = _MOCK_BALANCES.get(txn.account_id, 1000.00)

    if txn.transaction_type in ["withdrawal", "payment", "transfer"]:
        if current_balance < txn.amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient funds: balance is {current_balance}, attempted {txn.amount}",
            )
        new_balance = current_balance - txn.amount
    elif txn.transaction_type == "deposit":
        new_balance = current_balance + txn.amount
    else:
        new_balance = current_balance

    _MOCK_BALANCES[txn.account_id] = round(new_balance, 2)
    txn_id = f"TXN_{uuid.uuid4().hex[:12].upper()}"

    return {
        "transaction_id": txn_id,
        "account_id": txn.account_id,
        "transaction_reference": f"REF-{uuid.uuid4().hex[:8].upper()}",
        "amount": txn.amount,
        "currency": txn.currency,
        "transaction_type": txn.transaction_type,
        "status": "COMPLETED",
        "balance_after": round(new_balance, 2),
        "timestamp": datetime.utcnow(),
    }


@router.get("/{account_id}/balance")
def get_balance(account_id: str):
    if account_id not in _MOCK_BALANCES:
        _MOCK_BALANCES[account_id] = 2500.00
    return {
        "account_id": account_id,
        "balance": _MOCK_BALANCES[account_id],
        "currency": "USD",
        "as_of": datetime.utcnow(),
    }
