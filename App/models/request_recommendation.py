from App.database import db
from App.models import Notification
from sqlalchemy.sql import func
from datetime import datetime
import json
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

    def toJSON(self):
        return{
            'reqID': self.reqID,
            'staffID': self.staffID,
            'studentID': self.studentID,
            'deadline': self.deadline,
            'requestBody': self.requestBody,
            'status': self.status.value,
            'recommendation': self.Recommendation.toJSON() if self.Recommendation else None
        }
    
    def notify(self):
        notif = Notification(self.reqID, self.staffID)
        db.session.add(notif)
        db.session.commit()
    
    def set_status(self, status):
        isExpired = self.deadline < datetime.today()
        cannotModify = isExpired or (self.status !=  Status.PENDING)

        if cannotModify:
            return False

        values = [item.value for item in Status]
        if status in values:
            self.status = Status(status)
            db.session.add(self)
            db.session.commit()
            
        return True
    
    def complete_request(self):
        isExpired = self.deadline < datetime.today()
        canModify = not isExpired and (self.status ==  Status.ACCEPTED)

        if not canModify:
            return False
        
        self.status = Status.COMPLETED
        db.session.add(self)
        db.session.commit()
            
        return True