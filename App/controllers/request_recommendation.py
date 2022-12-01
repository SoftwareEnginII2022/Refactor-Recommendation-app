from App.models import Request_Recommendation, Student
from App.database import db
from sqlalchemy.exc import IntegrityError

def create_request(staffID, studentID, deadline, requestBody):
    newreq = Request_Recommendation(staffID, studentID, deadline, requestBody)
    return newreq

def send_request(reqID, staffID, comments):
    student = Student.query.get(staffID)
    newrec = create_request(reqID, staffID, comments)
    try:
        db.session.add(newrec)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return None

    # Should not need to append this, as the relationship will have it here already
    # student.Request.append(newrec)
    # try:
    #     db.session.add(student)
    #     db.session.commit()
    # except IntegrityError:
    #     db.session.rollback()
    #     return None
    # return student

def get_all_requests():
    return Request_Recommendation.query.all()

def get_all_requests_json():
    recs = get_all_requests()
    if not recs:
        return None
    recs = [rec.toJSON() for rec in recs]
    return recs

def get_request(reqID, recID):
    rec = Request_Recommendation.query.filter_by(reqID=reqID, recID=recID).first()
    if rec:
        return rec.toJSON()
    return None



