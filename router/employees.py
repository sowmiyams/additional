from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session, joinedload
import models
from database import SessionLocal, engine
from models import Employee, Secondary_info

router = APIRouter(
    prefix='/employee',
    tags=['employee']
)

models.Base.metadata.create_all(bind=engine)


class EmployeeCreate(BaseModel):
    staff_name: str
    date_of_entry: str
    age: int = Field(lt=50, gt=18, description="Not eligible for the application")
    date_of_birth: str
    phone_number: str
    address: str
    gender: str
    course: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post('/')
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    new_employee = Employee(
        staff_name=employee.staff_name,
        date_of_entry=employee.date_of_entry,
        age=employee.age,
        date_of_birth=employee.date_of_birth,
        phone_number=employee.phone_number,
        address=employee.address,
        gender=employee.gender,
        course=employee.course
    )

    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee


@router.get('/all')
def get_employees(page: int = Query(1, gt=0), db: Session = Depends(get_db)):
    per_page = 5
    offset = (page - 1) * per_page

    employees = db.query(Employee).options(joinedload(Employee.secondary_info)).offset(offset).limit(per_page).all()
    return employees


@router.put('/{staff_id}')
def update_employee(staff_id: int, employee: EmployeeCreate, db: Session = Depends(get_db)):
    existing_employee = db.query(Employee).filter(Employee.staff_id == staff_id).first()

    if not existing_employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    existing_employee.staff_name = employee.staff_name
    existing_employee.date_of_entry = employee.date_of_entry
    existing_employee.age = employee.age
    existing_employee.date_of_birth = employee.date_of_birth
    existing_employee.phone_number = employee.phone_number
    existing_employee.address = employee.address
    existing_employee.gender = employee.gender
    existing_employee.course = employee.course

    db.commit()
    db.refresh(existing_employee)

    return existing_employee


@router.delete('/{staff_id}')
def delete_employee(staff_id: int, db: Session = Depends(get_db)):
    existing_employee = db.query(Employee).filter(Employee.staff_id == staff_id).first()

    if not existing_employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    # Check if secondary_info records exist for the employee
    secondary_info_count = db.query(Secondary_info).filter(Secondary_info.employee_id == staff_id).count()

    if secondary_info_count > 0:
        raise HTTPException(status_code=400, detail="Cannot delete employee. Secondary info exists.")

    # Delete the employee
    db.delete(existing_employee)
    db.commit()

    return {'message': 'Employee deleted successfully'}
