from fastapi import FastAPI
from database import engine
from router import employees, secondary_info
import models

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(employees.router)
app.include_router(secondary_info.router)
