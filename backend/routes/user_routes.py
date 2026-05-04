from typing import Annotated

import bcrypt
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.Database.database import get_db
from backend.Database.models import User
from backend.schema import AuthResponse, UserCreate, UserLogin, UserSummary

router = APIRouter(prefix="/api/users", tags=["users"])
db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/signup", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: db_dependency):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists",
        )

    hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())
    new_user = User(username=user.username, password=hashed_password, role=user.role)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return AuthResponse(
        message="User created successfully",
        user=UserSummary.model_validate(new_user),
    )


@router.post("/signin", response_model=AuthResponse)
def login(user: UserLogin, db: db_dependency):
    user_in_db = db.query(User).filter(User.username == user.username).first()
    if not user_in_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    is_valid = bcrypt.checkpw(
        user.password.encode("utf-8"),
        user_in_db.password,
    )
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    return AuthResponse(
        message="Login successful",
        user=UserSummary.model_validate(user_in_db),
    )


@router.get("/", response_model=list[UserSummary])
def list_users(db: db_dependency):
    users = db.query(User).order_by(User.username.asc()).all()
    return [UserSummary.model_validate(user) for user in users]
