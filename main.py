import uvicorn
from server.model import PostSchema
from fastapi import FastAPI

server = FastAPI()

@server.get("/")
def index():
    return {"name":"First Data"}