import uvicorn
from fastapi import FastAPI

server = FastAPI()

@server.get("/")
def index():
    return {"name":"First Data"}