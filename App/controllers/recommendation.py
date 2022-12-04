from App.models import Recommendation, Student, Status
from App.database import db
from sqlalchemy.exc import IntegrityError
from App.controllers import (
    get_request,
    get_staff,
    get_student
)

def create_recommendation(reqID, staffID, comments):
    req = get_request(reqID)

    if req and req.status == Status.ACCEPTED:
        newrec = Recommendation(reqID=reqID, staffID=staffID, comments=comments)
        db.session.add(newrec)
        db.session.commit()
        req.complete_request()

        return True

    return False

def get_recommendation(recID):
    rec = Recommendation.query.get(recID)

    if not rec:
        return None
        
    rec.Staff = get_staff(rec.staffID)
    rec_req = get_request(rec.reqID)
    rec.Student = get_student(rec_req.studentID)

    return rec

def get_recommendation_by_request(reqID):
    rec = Recommendation.query.filter_by(reqID=reqID).first()

    if not rec:
        return None
        
    rec.Staff = get_staff(rec.staffID)

    return rec