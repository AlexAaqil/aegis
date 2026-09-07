# AEGIS BACKEND — TECHNICAL OVERVIEW (MVP v1.0)

## Purpose
Aegis is an offline-capable **fraud detection and biometric verification backend** designed for financial systems.  
It combines:
- Lightweight **biometric verification** (face + voice)
- **Rule-based fraud scoring**
- **Alert logging and admin analytics**
- Built with **FastAPI + SQLModel + Poetry**

## MODULE OVERVIEW

### 1. Biometric Engine (`biometric_service.py`)
Handles **face and voice enrollment + verification**.

**Endpoints**
- `POST /biometric/enroll` — stores encrypted feature vector
- `POST /biometric/verify` — compares new sample vs enrolled data

**Process**
1. Face/voice is captured (via webcam or mic)
2. Feature vector extracted → encrypted → stored in `data/biometrics/`
3. Verification compares cosine similarity (threshold = 0.85)

**Tech**
- OpenCV, NumPy, Pillow, SoundDevice
- Encryption via Fernet (Cryptography)
- Cosine similarity = trust score

---

### 2️. Fraud Engine (`fraud_service.py`)
Performs **risk analysis** for transactions using rule-based heuristics.

**Endpoint**
- `POST /fraud/analyze/{transaction_id}`

**Inputs**
- Transaction data (amount, time, location, device)
- Biometric verification result

**Logic**
| Rule | Condition | Risk Points |
|------|------------|-------------|
| Biometric Failed | `verified=False` | +30 |
| High Amount | > 5000 | +40 |
| Odd Hour | <6 or >22 | +20 |
| Unusual Location | outside allowed list | +25 |
| Unknown Device | `"unknown"` in device | +10 |

**Outputs**
```json
{
  "score": 90,
  "level": "high",
  "reasons": ["High transaction amount", "Odd-hour transaction"]
}
```

Stored Alerts

Alerts automatically created for medium or high risk scores.

---

### 3. Dashboard & Analytics (dashboard_service.py)

Gives the admin a view of fraud metrics and system performance.

Endpoints

- GET /dashboard/stats — summary metrics
- GET /dashboard/alerts — list all alerts
- GET /dashboard/alerts/{id} — single alert details

Example Response:
```json
{
  "total_transactions": 120,
  "total_alerts": 42,
  "high_risk_alerts": 12,
  "medium_risk_alerts": 18
}
```

## Database Models
```
users {
    id,
    name,
    email,
    password,
    role,
    is_active,
}

transactions {
    id,
    user_id,
    amount,
    device,
    location,
    timestamp,
    biometric_verified,
}

alerts {
    id,
    transaction_id,
    user_id,
    risk_level,
    score,
    reasons,
    created_at,
}
```

## Tech Stack
| Component | Technology |
|------|------------|
| Language | Python 3.11 |
| Framework | FastAPI |
| ORM	SQLModel | (SQLAlchemy + Pydantic) |
| Database | SQLite (can switch to PostgreSQL) |
| CLI | Typer |
| Package Manager | Poetry |
| ML (planned) | scikit-learn |

## Commands Quick Reference
| Action | Command |
|------|------------|
| Run backend | poetry run uvicorn app.main:app --reload |
| Test biometric locally | poetry run python app/tools/capture_live.py |
