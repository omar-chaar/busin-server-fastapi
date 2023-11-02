from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import URL_DATABASE

metadata = Base.metadata

engine = create_engine(URL_DATABASE)

SessionLocal = SessionLocal(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()