import random
from datetime import datetime
from app.models import Alert
from app.database import get_session

def compute_risk_score(transaction: dict, biometric_verified: bool) -> dict:
    """
    Compute a risk score for a transaction using basic heuristic rules.
    Returns a dictionary with risk level and explanations.

    This function:
    Takes transaction data + biometric verification result.
    Returns a structured risk evaluation:
    {
        "score": int (0-100),
        "level": str ("low", "medium", "high"),
        "reasons": list of str
    }
    Example:
    {
        "score": 72,
        "level": "high",
        "reasons": ["High transaction amount", "Odd-hour transaction"]
    }
    """

    amount = transaction.get("amount", 0)
    location = transaction.get("location", "unknown")
    time_str = transaction.get("timestamp", "")
    device = transaction.get("device", "unknown")

    # Start at neutral
    score = 0
    reasons = []

    # 1️⃣ Biometric factor
    if not biometric_verified:
        score += 30
        reasons.append("Biometric verification failed or missing")

    # 2️⃣ Amount factor
    if amount > 5000:
        score += 40
        reasons.append(f"High transaction amount (Ksh {amount})")

    # 3️⃣ Time factor
    if time_str:
        # Ensure compatibility whether timestamp is a string or datetime
        if isinstance(time_str, datetime):
            hour = time_str.hour
        else:
            hour = datetime.fromisoformat(str(time_str)).hour

        if hour < 6 or hour > 22:
            score += 20
            reasons.append("Odd-hour transaction")

    # 4️⃣ Device/location factor
    if location not in ["Nairobi", "Mombasa", "Kisumu"]:
        score += 25
        reasons.append(f"Unusual location: {location}")
    if "unknown" in device.lower():
        score += 10
        reasons.append("Unrecognized device")

    # Add some small random variance for realism
    score += random.randint(-3, 3)
    score = max(0, min(score, 100))

    # Categorize risk level
    if score < 30:
        level = "low"
    elif score < 70:
        level = "medium"
    else:
        level = "high"

    return {
        "score": score,
        "level": level,
        "reasons": reasons,
    }

def analyze_and_record_alert(transaction, session):
    """Analyze risk and create alert if risk is medium or high."""
    result = compute_risk_score(transaction.dict(), transaction.biometric_verified)

    if result["level"] in ["medium", "high"]:
        alert = Alert(
            transaction_id=transaction.id,
            user_id=transaction.user_id,
            risk_level=result["level"],
            score=result["score"],
            reasons=", ".join(result["reasons"])
        )
        session.add(alert)
        session.commit()

    return result
