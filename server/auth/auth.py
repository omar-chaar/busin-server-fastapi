from fastapi import APIRouter, Depends
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

SECRET_KEY = "verysecretkey"
ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/auth/token")

class CreateUserRequest(Basemodel):
    username: str
    password: str

class Token(Basemodel):
    access_token: str
    token_type: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated(Session, Depends(get_db))

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(request: CreateUserRequest, db: Session = db_dependency):
    create_user_model = Users(username=request.username, password=bcrypt_context.hash(request.password))
    
    db.add(create_user_model)
    db.commit()