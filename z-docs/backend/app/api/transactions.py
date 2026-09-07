from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from app.models import Transaction
from app.database import get_session

router = APIRouter(prefix="/transactions", tags=["Transactions"])

@router.post("/", response_model=Transaction)
def create_transaction(tx: Transaction, session=Depends(get_session)):
    session.add(tx)
    session.commit()
    session.refresh(tx)
    return tx

@router.get("/", response_model=list[Transaction])
def list_transactions(session=Depends(get_session)):
    return session.exec(select(Transaction)).all()
