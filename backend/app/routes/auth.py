from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.auth_schema import UserCreate, UserLogin, UserOut, Token
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=Token)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    return AuthService.register_user(db, user_in)

@router.post("/login", response_model=Token)
def login(user_in: UserLogin, db: Session = Depends(get_db)):
    return AuthService.login_user(db, user_in)

@router.get("/me", response_model=UserOut)
def get_me(db: Session = Depends(get_db)):
    user = db.query(User).first()
    if not user:
        user = User(email="admin@supplyprescript.com", hashed_password="password", full_name="Supply Chain Lead", role="Director")
        db.add(user)
        db.commit()
        db.refresh(user)
    return UserOut.model_validate(user)
