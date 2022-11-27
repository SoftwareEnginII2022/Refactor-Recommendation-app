from App.models import Recommendation, Student
from App.database import db
from sqlalchemy.exc import IntegrityError

def create_recommendation(reqID, staffID, comments):
    newrec = Recommendation(reqID=reqID, staffID=staffID, comments=comments)
    return newrec

def send_recommendation(reqID, staffID, comments):
    student = Student.query.get(staffID)
    newrec = create_recommendation(reqID, staffID, comments)
    try:
        db.session.add(newrec)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return None

    # Should not need to append this, as the relationship will have it here already
    # student.Recommendation.append(newrec)
    # try:
    #     db.session.add(student)
    #     db.session.commit()
    # except IntegrityError:
    #     db.session.rollback()
    #     return None
    # return student

def get_all_recommendations():
    return Recommendation.query.all()

def get_all_recommendations_json():
    recs = get_all_recommendations()
    if not recs:
        return None
    recs = [rec.toJSON() for rec in recs]
    return recs

def get_recommendation(reqID, recID):
    rec = Recommendation.query.filter_by(reqID=reqID, recID=recID).first()
    if rec:
        return rec.toJSON()
    return None



