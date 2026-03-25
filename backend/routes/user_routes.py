from fastapi import APIRouter,Depends,HTTPException,status
from typing import Annotated
from sqlalchemy.orm import Session
import bcrypt


from backend.schema import UserCreate,UserValidate
from backend.Database.database import get_db,SessionLocal
from backend.Database.models import User
router = APIRouter()


db_dependency = Annotated[Session,Depends(get_db)]
@router.post('/signup')
def create_user(user:UserCreate , db:db_dependency):
    password = user.password

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'),salt)

    new_user = User(username=user.username,password =hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"detail":"User created succesfully"}

@router.post('/signin')
def login(user:UserValidate, db : db_dependency):
    user_in_db = db.query(User).filter(User.username == user.username).first()
    if not user_in_db :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    is_valid = bcrypt.checkpw(user.password.encode('utf-8'),hashed_password=user_in_db.password)
    
    if not is_valid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return {"message":"Login succesfull"}