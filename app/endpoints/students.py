from fastapi import APIRouter, HTTPException, Depends

from app.schemas.student_schema import Student
from app.database import crud
from app.database.setup import get_db

students_router = APIRouter(
    prefix='/students'
)


@students_router.get('/', response_model=Student)
async def get_student(student_id: int, db=Depends(get_db)):
    student = crud.get_student_by_id(db=db, student_id=student_id)
    if student is None:
        raise HTTPException(
            status_code=400,
            detail=f'Could not find student with id <{student_id}>'
        )
    return student
