from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Transaction(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int
    amount: float
    location: str
    device: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    biometric_verified: bool = Field(default=False)
    risk_score: float | None = None
    risk_level: str | None = None

class Alert(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    transaction_id: int
    user_id: int
    risk_level: str
    score: int
    reasons: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
