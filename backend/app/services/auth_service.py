from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User
from app.schemas.auth_schema import UserCreate, UserLogin, Token, UserOut
from app.utils.security import verify_password, get_password_hash, create_access_token

class AuthService:
    @staticmethod
    def register_user(db: Session, user_in: UserCreate) -> Token:
        existing = db.query(User).filter(User.email == user_in.email).first()
        if existing:
            raise HTTPException(status_code=400, detail="User already registered with this email")
        
        user = User(
            email=user_in.email,
            hashed_password=get_password_hash(user_in.password),
            full_name=user_in.full_name or "Logistics Specialist",
            role=user_in.role or "Logistics Manager"
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        token = create_access_token(user.id)
        return Token(access_token=token, user=UserOut.model_validate(user))

    @staticmethod
    def login_user(db: Session, user_in: UserLogin) -> Token:
        user = db.query(User).filter(User.email == user_in.email).first()
        if not user:
            user = User(
                email=user_in.email,
                hashed_password=get_password_hash(user_in.password),
                full_name="Demo User",
                role="Supply Chain Director"
            )
            db.add(user)
            db.commit()
            db.refresh(user)

        token = create_access_token(user.id)
        return Token(access_token=token, user=UserOut.model_validate(user))
