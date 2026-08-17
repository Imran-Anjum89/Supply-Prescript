from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import UserCreate, UserLogin, UserOut, Token
import datetime

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=Token)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user_in.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="User with this email already exists")
    
    # Store user (demo password handling)
    user = User(
        email=user_in.email,
        hashed_password=user_in.password,
        full_name=user_in.full_name or "Logistics Manager",
        role=user_in.role or "Logistics Manager"
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token_str = f"demo_jwt_token_for_{user.id}"
    return Token(access_token=token_str, user=UserOut.model_validate(user))

@router.post("/login", response_model=Token)
def login(user_in: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_in.email).first()
    if not user:
        # Create user automatically for seamless demo experience if registering via login form
        user = User(
            email=user_in.email,
            hashed_password=user_in.password,
            full_name="Demo User",
            role="Supply Chain Director"
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    
    token_str = f"demo_jwt_token_for_{user.id}"
    return Token(access_token=token_str, user=UserOut.model_validate(user))

@router.get("/me", response_model=UserOut)
def get_me(db: Session = Depends(get_db)):
    user = db.query(User).first()
    if not user:
        user = User(email="admin@supplyprescript.com", hashed_password="password", full_name="Supply Chain Lead", role="Director")
        db.add(user)
        db.commit()
        db.refresh(user)
    return UserOut.model_validate(user)
