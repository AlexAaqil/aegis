from fastapi import APIRouter, Depends
from sqlmodel import select
from app.models import Alert
from app.database import get_session

router = APIRouter(prefix="/alerts", tags=["Alerts"])

@router.get("/", response_model=list[Alert])
def list_alerts(session=Depends(get_session)):
    return session.exec(select(Alert)).all()
