from fastapi import APIRouter
from passlib.context import CryptContext

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

SECRET_KEY = "verysecretkey"
ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
