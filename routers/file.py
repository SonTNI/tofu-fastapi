from fastapi import File, UploadFile, APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List
from database import db_dependency
import models
import csv
import io
from io import TextIOWrapper

router = APIRouter(
    prefix="/file",
    tags=["File"],
    responses={404: {"message": "Not found"}}
)

@router.post("/import")
async def import_file(db: db_dependency, csv_file: UploadFile = File(...)):
    contents = await csv_file.read()
    text_io_wrapper = TextIOWrapper(io.BytesIO(contents), encoding='utf-8')
    
    reader = csv.DictReader(text_io_wrapper)
    data = [row for row in reader]
    
    insert_data(db, data)
    
    return {"message": "CSV data imported successfully"}

@router.post("/imports")
async def import_multi_file(files: List[UploadFile] = File(...)):
    file = [
        {
            "File Name":file.filename, 
            "Size":len(await file.read())
        } 
        for file in files
        ]
    return  file

@router.get("/export")
async def export_file(db: db_dependency):
    db_applicant = db.query(models.Applicant).all()
    return StreamingResponse(
            iter([generate_csv(db_applicant)]),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename=data.csv"}
    )
    
def insert_data(db: Session, data):
    db.query(models.Applicant).delete()
    for row in data:
        db_row = models.Applicant(**row)
        db_applicant = db.query(models.Applicant).filter(db_row.id == models.Applicant.id).first()
        if db_applicant is None:
            new_applicant = models.Applicant(
            id = db_row.id,
            firstname = db_row.firstname,
            lastname = db_row.lastname,
            email = db_row.email,
            address = db_row.address,
            expected_salary = db_row.expected_salary
            )
            db.add(new_applicant)
        else:
            db_applicant.firstname = db_row.firstname
            db_applicant.lastname = db_row.lastname
            db_applicant.email = db_row.email
            db_applicant.address = db_row.address
            db_applicant.expected_salary = db_row.expected_salary
    db.commit()

def generate_csv(data: List[models.Applicant]):
    csv_buffer = io.StringIO()
    writer = csv.DictWriter(csv_buffer, fieldnames=["id", "firstname", "lastname", "email", "address", "expected_salary"])
    writer.writeheader()
    
    for applicant in data:
        writer.writerow(
            {
                "id": applicant.id, 
                "firstname": applicant.firstname, 
                "lastname": applicant.lastname, 
                "email": applicant.email,
                "address": applicant.address,
                "expected_salary": applicant.expected_salary,
            }
        )
    
    csv_buffer.seek(0)
    return csv_buffer.getvalue()