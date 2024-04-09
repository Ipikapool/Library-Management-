from fastapi import FastAPI
from routes.student import student


app = FastAPI()
app.include_router(student)

