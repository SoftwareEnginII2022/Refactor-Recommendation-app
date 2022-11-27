from App.models import Student
from App.database import db

def get_student(id):
    student = Student.query.get(id)
    if student:
        return student
    return None

def get_all_students():
    return Student.query.all()

def get_all_students_json():
    students = get_all_students()
    if not students:
        return None
    students = [student.toJSON() for student in students]
    return students

def get_student_request_list(studentID):
    student = get_student(studentID)
    return student.Requests

def get_student_request_json(studentID):
    reqs = get_student_request_list(studentID)
    if reqs:
        return [req.toJSON() for req in reqs]
    return None