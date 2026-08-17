import re
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User
from app.schemas.auth_schema import UserCreate, UserLogin, Token, UserOut
from app.utils.security import verify_password, get_password_hash, create_access_token

def is_valid_email(email: str) -> bool:
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return bool(re.match(pattern, email))

class AuthService:
    @staticmethod
    def register_user(db: Session, user_in: UserCreate) -> Token:
        clean_email = user_in.email.strip().lower()
        if not is_valid_email(clean_email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email format")
        
        if len(user_in.password.strip()) < 6:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password must be at least 6 characters long")

        existing = db.query(User).filter(User.email == clean_email).first()
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="An account with this email already exists")
        
        user = User(
            email=clean_email,
            hashed_password=get_password_hash(user_in.password.strip()),
            full_name=user_in.full_name or "Logistics Specialist",
            role=user_in.role or "Planner"
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        token = create_access_token(user.id)
        return Token(access_token=token, user=UserOut.model_validate(user))

    @staticmethod
    def login_user(db: Session, user_in: UserLogin) -> Token:
        clean_email = user_in.email.strip().lower()
        user = db.query(User).filter(User.email == clean_email).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        if not verify_password(user_in.password.strip(), user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        token = create_access_token(user.id)
        return Token(access_token=token, user=UserOut.model_validate(user))
