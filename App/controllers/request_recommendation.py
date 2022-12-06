from App.models import Request_Recommendation, Student, Status
from App.database import db
from App.controllers import get_user, get_staff
from sqlalchemy.exc import IntegrityError
from datetime import datetime

def create_request(staffID, studentID, deadline, requestBody):
    query = Request_Recommendation.query.filter(Request_Recommendation.staffID == staffID,Request_Recommendation.studentID == studentID, db.or_(Request_Recommendation.status == Status.PENDING, Request_Recommendation.status == Status.ACCEPTED)).all()
    if not query: 
        newreq = Request_Recommendation(staffID, studentID, deadline, requestBody)
        try:
            db.session.add(newreq)
            db.session.commit()
            newreq.notify()
            return newreq
        except IntegrityError:
            db.session.rollback()
            return None
    return None

def get_student_requests(id):
    check_expired_requests()
    requests = Request_Recommendation.query.filter_by(studentID = id).all()
    if not requests:
        return None

    for req in requests:
        req.Staff = get_staff(req.staffID)

    return requests

def get_request(reqID):
    check_expired_requests()
    return Request_Recommendation.query.get(reqID)

def get_accepted_request_by_staffID(staffID):
    check_expired_requests()
    requests = Request_Recommendation.query.filter(Request_Recommendation.status == (Status.ACCEPTED), staffID==staffID).all()

    for req in requests:
        req.Student = get_user(req.studentID)
    
    return requests

def accept_request(reqID):
    req = get_request(reqID)
    if req:
        return req.set_status(Status.ACCEPTED)
    return False


def reject_request(reqID):
    req = get_request(reqID)
    if req:
        return req.set_status(Status.REJECTED)
    return False


def cancel_request(reqID):
    req = get_request(reqID)
    if req:
        return req.cancel_request()
    return False

def check_expired_requests():
    req_recs = Request_Recommendation.query.filter(Request_Recommendation.deadline < datetime.today()).all()

    for req_rec in req_recs:
        req_rec.reject_expired_request()