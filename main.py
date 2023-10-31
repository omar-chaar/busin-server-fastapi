import uvicorn
from model import PostSchema
from fastapi import FastAPI
import auth

server = FastAPI()
server.include_router(auth.router)

@server.get("/")
def index():
    return {"name":"First Data"}