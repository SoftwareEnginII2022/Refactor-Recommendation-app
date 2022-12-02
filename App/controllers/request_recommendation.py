from App.models import Request_Recommendation, Student, Status
from App.database import db
from sqlalchemy.exc import IntegrityError

def create_request(staffID, studentID, deadline, requestBody):
    query = Request_Recommendation.query.filter(Request_Recommendation.staffID == staffID,Request_Recommendation.studentID == studentID, db.or_(Request_Recommendation.status == Status.PENDING, Request_Recommendation.status == Status.ACCEPTED)).all()
    if query == []:       
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

def get_all_student_requests(id):
    request = Request_Recommendation.query.filter_by(studentID = id)
    if not request:
        return None
    return request

def get_all_requests_json():
    recs = get_all_requests()
    if not recs:
        return None
    recs = [rec.toJSON() for rec in recs]
    return recs

def get_all_student_requests_json(id):
    recs = get_all_student_requests(id)
    if not recs:
        return None
    recs = [rec.toJSON() for rec in recs]
    return recs

def get_request(reqID):
    return Request_Recommendation.query.get(reqID)

def get_request_json(reqID):
    rec = get_request(reqID)
    if rec:
        return rec.toJSON()
    return None

def accept_request(reqID):
    req = get_request(reqID)
    if req:
        return req.set_status("accepted")
    return False


def reject_request(reqID):
    req = get_request(reqID)
    if req:
        return req.set_status("rejected")
    return False