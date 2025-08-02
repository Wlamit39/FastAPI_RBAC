from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.db.models import User
from app.db.database import get_session
from app.schemas.user import UserCreate, UserLogin, UserResponse, TokenResponse
from app.core.security import hash_password, verify_password, create_access_token
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(tags=["Authentication"])


@router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate, session: Session = Depends(get_session)):
    # Check if username exists
    existing_user = session.exec(select(User).where(User.username == user_data.username)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    # Hash password and save user
    new_user = User(
        username=user_data.username,
        hashed_password=hash_password(user_data.password),
        role=user_data.role
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


@router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    # Fetch user by username
    user = session.exec(select(User).where(User.username == form_data.username)).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # Create JWT
    token = create_access_token({"sub": str(user.id), "role": user.role})
    return {"access_token": token, "token_type": "bearer"}
