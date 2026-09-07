from sqlmodel import SQLModel, create_engine, Session
from app.config import settings

engine = create_engine(settings.DB_URL, connect_args={"check_same_thread": False})

def init_db():
    import app.models  # ensures models are imported before creating tables
    SQLModel.metadata.create_all(engine)
    print("[INFO] Database initialized at:", settings.DB_URL)

def get_session() -> Session:
    return Session(engine)
