from bson import ObjectId
from fastapi import APIRouter, HTTPException

from models.student import Student
from config.db import conn
from schemas.students import student_entity, students_entity
student = APIRouter()


@student.get('/')
async def library_management():
    return "Welcome"


@student.post('/students', status_code=201)
async def create_user(student: Student):
    student_data = student.dict(exclude_unset=True)

    if not student_data.get("name") or not student_data.get("age") or not student_data.get("address"):
        raise HTTPException(status_code=400, detail="Name, age, and address are required")

    address_data = student_data.get("address")
    if not address_data.get("city") or not address_data.get("country"):
        raise HTTPException(status_code=400, detail="City and country are required in the address")

    inserted_student = conn.students.student.insert_one(student.dict())
    inserted_id = inserted_student.inserted_id

    return str(inserted_id)


@student.get('/students')
async def find_users_with_country_age(country: str | None = None, age: int | None = None):
    query = {}
    projection = {'_id': 0, 'name': 1, 'age': 1}

    if country is not None and age is not None:
        query = {"address": {"$exists": True}, "address.country": country, "age": {"$gte": age}}
    elif country is not None:
        query = {"address": {"$exists": True}, "address.country": country}
    elif age is not None:
        query = {"age": {"$gte": age}}

    docs = conn.students.student.find(query, projection)

    result = []
    for doc in docs:
        result.append(doc)

    return result


@student.get('/students/{id}')
async def get_student_by_id(id: str):
    student = conn.students.student.find_one({"_id": ObjectId(id)})

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    return student_entity(student)


@student.delete('/students/{id}')
async def delete_student(id: str):
    student = conn.students.student.find_one({"_id": ObjectId(id)})

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    student_entity(conn.students.student.find_one_and_delete({"_id": ObjectId(id)}))


@student.patch('/students/{id}', status_code=204)
async def patch_student(id: str, student: Student):
    old_student = conn.students.student.find_one({"_id": ObjectId(id)})

    if not old_student:
        raise HTTPException(status_code=404, detail="Student not found")

    conn.students.student.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": student.dict(exclude_unset=True)}
    )
