from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import applicant, file
from database import engine, SessionLocal

import models

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
models.Base.metadata.create_all(bind=engine)

app.include_router(applicant.router)
app.include_router(file.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}
