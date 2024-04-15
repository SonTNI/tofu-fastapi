from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database import db_dependency
import models

router = APIRouter(
    prefix="/applicant",
    tags=["Applicant"],
    responses={404: {"message": "Not found"}}
)

class Applicant(BaseModel):
    firstname: str
    lastname: str
    email: str
    address: str
    expected_salary: int
    
@router.get("/")
async def get_applicants(db: db_dependency):
    db_applicant = db.query(models.Applicant).all()
    return db_applicant

@router.get("/{applicant_id}")
async def get_applicant(applicant_id: int, db: db_dependency):
    db_applicant = db.query(models.Applicant).filter(applicant_id == models.Applicant.id).first()
    if db_applicant is None:
        raise HTTPException(status_code=404, detail='Applicant not found')
    return db_applicant

@router.post("/")
async def create_applicant(applicant: Applicant, db: db_dependency):
    db_applicant = models.Applicant(**applicant.model_dump())
    db.add(db_applicant)
    db.commit()
    return db_applicant

@router.put("/{applicant_id}")
async def edit_applicant(applicant_id: int, applicant: Applicant, db: db_dependency):
    db_applicant = db.query(models.Applicant).filter(applicant_id == models.Applicant.id).first()
    if db_applicant is None:
        raise HTTPException(status_code=404, detail='Applicant not found')
    db_applicant.firstname = applicant.firstname
    db_applicant.lastname = applicant.lastname
    db_applicant.email = applicant.email
    db_applicant.address = applicant.address
    db_applicant.expected_salary = applicant.expected_salary
    db.commit()
    return applicant

@router.delete("/{applicant_id}")
async def delete_applicant(applicant_id: int, db: db_dependency):
    db_applicant = db.query(models.Applicant).filter(applicant_id == models.Applicant.id).first()
    if db_applicant is None:
        raise HTTPException(status_code=404, detail='Applicant not found')
    db.delete(db_applicant)
    db.commit()
    return db_applicant