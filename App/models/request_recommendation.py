from App.database import db
from datetime import date
from App.models import Notification
from sqlalchemy.sql import func

from enum import Enum
class Status(Enum):
    PENDING = "Pending"
    ACCEPTED = "Accepted"
    REJECTED = "Rejected"
    COMPLETED = "Completed"
    EXPIRED = "Expired"

class Request_Recommendation(db.Model):
    __tablename__ = "request_recommendation"
    reqID = db.Column(db.Integer, primary_key=True)
    staffID = db.Column(db.Integer, db.ForeignKey('staff.staffID'))
    studentID = db.Column(db.Integer, db.ForeignKey('student.studentID'))
    dateRequested = db.Column(db.Date, nullable=False, default=date.today)
    deadline = db.Column(db.Date, nullable= False, default= date(1970,1,1))
    status = db.Column(db.Enum(Status), nullable = False)
    requestBody = db.Column(db.String, nullable=False)

    Recommendation = db.relationship('Recommendation', uselist=True, backref='request_recommendation', lazy=True, cascade="all, delete-orphan")

    def __init__(self, staffID, studentID, deadline, requestBody):
        self.staffID = staffID
        self.studentID = studentID
        self.deadline = deadline
        self.dateRequested = date.today()       
        self.requestBody=requestBody
        self.status=Status.PENDING

        self.notify()

    def toJSON(self):
        return{
            'id': self.reqID,
            'staffID': self.staffID,
            'studentID': self.studentID,
            'dateRequested':self.dateRequested,
            'deadline': self.deadline,
            'status': self.status.value,
            'requestBody': self.requestBody,
            'status': self.status,
            'recommendation': self.Recommendation.toJSON() if self.Recommendation else None
        }
    
    def notify(self):
        notif = Notification(self.reqID, self.staffID)
        pass
    