from sqlmodel import select, func
from app.models import Transaction
from app.models import Alert

def get_dashboard_stats(session):
    """Return fraud overview metrics for admin dashboard."""
    total_tx = session.exec(select(func.count(Transaction.id))).one()
    total_alerts = session.exec(select(func.count(Alert.id))).one()

    high_risk = session.exec(
        select(func.count(Alert.id)).where(Alert.risk_level == "high")
    ).one()

    medium_risk = session.exec(
        select(func.count(Alert.id)).where(Alert.risk_level == "medium")
    ).one()

    return {
        "total_transactions": total_tx,
        "total_alerts": total_alerts,
        "high_risk_alerts": high_risk,
        "medium_risk_alerts": medium_risk,
    }
