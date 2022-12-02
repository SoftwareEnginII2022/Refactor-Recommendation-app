from App.database import db
from sqlalchemy.sql import func
from datetime import datetime

class Recommendation(db.Model):
    recID = db.Column(db.Integer, primary_key=True)
    staffID = db.Column(db.Integer, db.ForeignKey('staff.staffID'))
    reqID = db.Column(db.Integer, db.ForeignKey('request_recommendation.reqID'))
    dateSubmitted = db.Column(db.Date, nullable=False, default=func.now())
    comments = db.Column(db.String, nullable=False)

    def __init__(self, reqID, staffID, comments):
        self.reqID=reqID
        self.staffID=staffID
        self.dateSubmitted = datetime.today()
        self.comments=comments
    
    def toJSON(self):
        return{
            'recID': self.recID,
            'reqID': self.reqID,
            'staffID': self.staffID,
            'dateSubmitted':self.dateSubmitted,
            'comments': self.comments
        }

    
