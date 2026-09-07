from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.database import get_session
from app.models import Alert
from app.services.dashboard_service import get_dashboard_stats

router = APIRouter(prefix="/dashboard", tags=["Admin Dashboard"])

@router.get("/stats")
def dashboard_stats(session: Session = Depends(get_session)):
    """Return summary stats for the dashboard."""
    return get_dashboard_stats(session)

@router.get("/alerts")
def list_alerts(session: Session = Depends(get_session)):
    """List all fraud alerts."""
    alerts = session.exec(select(Alert)).all()
    return alerts

@router.get("/alerts/{alert_id}")
def get_alert(alert_id: int, session: Session = Depends(get_session)):
    """Get details of a specific alert."""
    alert = session.get(Alert, alert_id)
    if not alert:
        return {"error": "Alert not found"}
    return alert
