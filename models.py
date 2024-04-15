from sqlalchemy import Column, Integer, String, Double
from database import Base

class Applicant(Base): 
    __tablename__ = 'applicant'
    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String(255))
    lastname = Column(String(255))
    email = Column(String(255))
    address = Column(String(255))
    expected_salary = Column(Integer)
    