from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="PayFlex API",
    description="API de services financiers",
    version="1.0.0"
)

# Base de données temporaire pour le TP
accounts = {
    "123": 1000.0,
    "456": 500.0
}


class Payment(BaseModel):
    account_id: str
    amount: float = Field(gt=0)


@app.get("/")
def home():
    return {"message": "Welcome to PayFlex API"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/accounts/{account_id}/balance")
def get_balance(account_id: str):

    if account_id not in accounts:
        raise HTTPException(
            status_code=404,
            detail="Account not found"
        )

    return {
        "account_id": account_id,
        "balance": accounts[account_id]
    }


@app.post("/payments")
def make_payment(payment: Payment):

    if payment.account_id not in accounts:
        raise HTTPException(
            status_code=404,
            detail="Account not found"
        )

    if payment.amount > accounts[payment.account_id]:
        raise HTTPException(
            status_code=400,
            detail="Insufficient balance"
        )

    accounts[payment.account_id] -= payment.amount

    return {
        "message": "Payment successful",
        "account_id": payment.account_id,
        "remaining_balance": accounts[payment.account_id]
    }