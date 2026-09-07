from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from app.models import User
from app.database import get_session

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=User)
def create_user(user: User, session=Depends(get_session)):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@router.get("/", response_model=list[User])
def list_users(session=Depends(get_session)):
    users = session.exec(select(User)).all()
    return users
