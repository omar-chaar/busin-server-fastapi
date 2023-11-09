import uvicorn
from fastapi import FastAPI, Depends
import auth
from sqlalchemy.orm import Session
from sqlalchemy import text

app = FastAPI()

app.include_router(auth.router)

@app.get("/")
async def root(db: Session = Depends(auth.get_db)):
    # Check the database connection
    try:
        db.execute(text("SELECT 1"))
        return {"message": "API connected to the database"}
    except Exception as e:
        return {"message": f"Failed to connect to the database: {str(e)}"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)