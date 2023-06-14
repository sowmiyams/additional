
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey


class Employee(Base):
    __tablename__ = 'employees'

    staff_id = Column(Integer, primary_key=True, index=True)
    date_of_entry = Column(String)
    age = Column(Integer)
    staff_name = Column(String)
    date_of_birth = Column(String)
    phone_number = Column(String)
    address = Column(String)
    gender = Column(String)
    course = Column(String)

    secondary_info = relationship("Secondary_info", back_populates="employee", cascade="all, delete")

class Secondary_info(Base):
    __tablename__ = 'secondary_info'

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey('employees.staff_id'))
    position = Column(String)
    department = Column(String)
    salary = Column(Float)

    employee = relationship("Employee", back_populates="secondary_info")

