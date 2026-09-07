from fastapi import FastAPI
from app.database import init_db
from app.api import users, transactions, alerts, fraud, dashboard
from app.api import biometric

app = FastAPI(title="Aegis Backend (MVP)")

@app.on_event("startup")
def on_startup():
    init_db()

# mount route groups
app.include_router(users.router)
app.include_router(transactions.router)
app.include_router(alerts.router)
app.include_router(biometric.router)
app.include_router(fraud.router)
app.include_router(dashboard.router)

@app.get("/health")
def health():
    return {"status": "ok", "service": "aegis backend"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=False)
