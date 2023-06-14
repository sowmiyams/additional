from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session, relationship
import models
from database import SessionLocal, engine
from models import Employee, Secondary_info

router = APIRouter(
    prefix='/secondary_info',
    tags=['secondary_info']
)

models.Base.metadata.create_all(bind=engine)


class Secondary_infoCreate(BaseModel):
    department: str
    position: str
    salary: float


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post('/{staff_id}')
def create_secondary_info(staff_id: int, secondary_info: Secondary_infoCreate, db: Session = Depends(get_db)):
    existing_secondary_info = db.query(Secondary_info).filter(Secondary_info.employee_id == staff_id).first()

    if existing_secondary_info:
        raise HTTPException(status_code=400, detail="Secondary info already exists for the employee")

    existing_employee = db.query(Employee).filter(Employee.staff_id == staff_id).first()

    if not existing_employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    new_secondary_info = Secondary_info(
        employee_id=staff_id,
        position=secondary_info.position,
        department=secondary_info.department,
        salary=secondary_info.salary
    )

    db.add(new_secondary_info)
    db.commit()
    db.refresh(new_secondary_info)

    return new_secondary_info


Employee.secondary_info = relationship("Secondary_info", back_populates="employee")

Secondary_info.employee = relationship("Employee", back_populates="secondary_info")


@router.put('/{staff_id}')
def update_secondary_info(staff_id: int, secondary_info: Secondary_infoCreate, db: Session = Depends(get_db)):
    existing_employee = db.query(Employee).filter(Employee.staff_id == staff_id).first()

    if not existing_employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    existing_secondary_info = db.query(Secondary_info).filter(Secondary_info.employee_id == staff_id).first()

    if not existing_secondary_info:
        raise HTTPException(status_code=404, detail="SecondaryInfo not found")

    existing_secondary_info.position = secondary_info.position
    existing_secondary_info.department = secondary_info.department
    existing_secondary_info.salary = secondary_info.salary

    db.commit()
    db.refresh(existing_secondary_info)

    return existing_secondary_info


@router.delete('/{staff_id}')
def delete_secondary_info(staff_id: int, db: Session = Depends(get_db)):
    existing_employee = db.query(Employee).filter(Employee.staff_id == staff_id).first()

    if not existing_employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    db.query(Secondary_info).filter(Secondary_info.employee_id == staff_id).delete()

    db.commit()

    return {'message': 'Secondary info deleted successfully'}
