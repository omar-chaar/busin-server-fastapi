from fastapi import APIRouter, Depends, FastAPI
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel
from starlette import status
from typing import Annotated
from database.database import SessionLocal
import database.models as models
from config import SECRET_KEY, ALGORITHM

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

ACCESS_TOKEN_EXPIRE_MINUTES = 20

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

class CreateUserRequest(BaseModel):
    user_id: str
    name: str
    surname: str
    position: str
    email: str
    password: str
    profile_picture: str
    department_id: int
    is_adm: bool
    is_owner: bool
    reg_code: str

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
    create_user_model = models.User(user_id=create_user_request.user_id, name=create_user_request.name, surname=create_user_request.surname, 
    position=create_user_request.position, email=create_user_request.email, password=bcrypt_context.hash(create_user_request.password), profile_picture=create_user_request.profile_picture, department_id=create_user_request.department_id,
     is_adm=create_user_request.is_adm, is_owner=create_user_request.is_owner, reg_code=create_user_request.reg_code)
    
    db.add(create_user_model)
    db.commit()

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: db_dependency):
    user = authenticate_user(db, form_data.email, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    token = create_access_token(user.username, user.id, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
def authenticate_user(db, email: str, password: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.password):
        return False
    return user  

def create_access_token(username: str, user_id: int, expires_delta: Optional[timedelta] = None):
    to_encode = {"username": username, "user_id": user_id}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt