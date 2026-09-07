from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from app.database import get_session
from app.models import Transaction
from app.services.fraud_service import analyze_and_record_alert

router = APIRouter(prefix="/fraud", tags=["Fraud Detection"])

@router.post("/analyze/{transaction_id}")
def analyze_transaction(transaction_id: int, session: Session = Depends(get_session)):
    transaction = session.exec(
        select(Transaction).where(Transaction.id == transaction_id)
    ).first()

    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    result = analyze_and_record_alert(transaction, session)

    return {
        "transaction_id": transaction.id,
        "user_id": transaction.user_id,
        "risk": result
    }
