from fastapi import APIRouter, Depends, FastAPI
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from pydantic import BaseModel
from starlette import status
from typing import Annotated
from database.database import SessionLocal
import database.models as models
from config import SECRET_KEY

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

class CreateUserRequest(BaseModel):
    user_id: str
    password: str    

class Token(BaseModel):
    access_token: str
    token_type: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    create_user_model = models.USER_AUTH(user_id=create_user_request.user_id, password=bcrypt_context.hash(create_user_request.password))
    
    db.add(create_user_model)
    db.commit()

