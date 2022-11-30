from App.database import db
from App.models import Notification
from sqlalchemy.sql import func
import enum

class Status(enum.Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    COMPLETED = "completed"

class Request_Recommendation(db.Model):
    __tablename__ = "request_recommendation"
    reqID = db.Column(db.Integer, primary_key=True)
    staffID = db.Column(db.Integer, db.ForeignKey('staff.staffID'))
    studentID = db.Column(db.Integer, db.ForeignKey('student.studentID'))
    deadline = db.Column(db.DateTime(timezone=True), nullable= False, default=func.now())
    requestBody = db.Column(db.String, nullable=False)
    status = db.Column(db.Enum(Status), nullable=False, default=Status.PENDING)
    Recommendation = db.relationship('Recommendation', single_parent=True, uselist=False, backref='request_recommendation', lazy=True, cascade="all, delete-orphan")

    def __init__(self, staffID, studentID, deadline, requestBody):
        self.staffID = staffID
        self.studentID = studentID
        self.deadline = deadline        
        self.requestBody=requestBody
        self.status=Status.PENDING

        self.notify()

    def toJSON(self):
        return{
            'id': self.reqID,
            'staffID': self.staffID,
            'studentID': self.studentID,
            'deadline': self.deadline,
            'requestBody': self.requestBody,
            'status': self.status,
            'recommendation': self.Recommendation.toJSON() if self.Recommendation else None
        }
    
    def notify(self):
        notif = Notification(self.reqID, self.staffID)
        pass
    