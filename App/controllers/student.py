from App.models import Student
from App.database import db

def get_student(id):
    student = Student.query.get(id)
    if student:
        return student
    return None