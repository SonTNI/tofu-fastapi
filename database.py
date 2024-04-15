from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from typing import Annotated

URL_DATABASE = 'sqlite:///./sql_app.db'

engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autoflush=False, bind=engine)

Base = declarative_base()

def get_database(): 
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_database)]