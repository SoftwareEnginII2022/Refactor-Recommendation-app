from App.database import db
from App.models import Notification
from sqlalchemy.sql import func
from datetime import datetime

from enum import Enum
class Status(Enum):
    PENDING = "Pending"
    ACCEPTED = "Accepted"
    REJECTED = "Rejected"
    COMPLETED = "Completed"
    EXPIRED = "Expired"
    CANCELLED = "Cancelled"

class Request_Recommendation(db.Model):
    __tablename__ = "request_recommendation"
    reqID = db.Column(db.Integer, primary_key=True)
    staffID = db.Column(db.Integer, db.ForeignKey('staff.staffID'))
    studentID = db.Column(db.Integer, db.ForeignKey('student.studentID'))
    dateRequested = db.Column(db.Date, nullable=False, default=func.now())
    deadline = db.Column(db.DateTime(timezone=True), nullable= False, default= func.now())
    status = db.Column(db.Enum(Status), nullable = False, default = Status.PENDING)
    requestBody = db.Column(db.String, nullable=False)

    Recommendation = db.relationship('Recommendation', uselist=False, backref='request_recommendation', lazy=True, cascade="all, delete-orphan")

    def __init__(self, staffID, studentID, deadline, requestBody):
        self.staffID = staffID
        self.studentID = studentID
        self.deadline = deadline
        self.dateRequested = datetime.today()
        self.requestBody=requestBody
        self.status=Status.PENDING

    def toJSON(self):
        return{
            'reqID': self.reqID,
            'staffID': self.staffID,
            'studentID': self.studentID,
            'dateRequested':self.dateRequested,
            'deadline': self.deadline,
            'status': self.status.value,
            'requestBody': self.requestBody,
            'recommendation': self.Recommendation.toJSON() if self.Recommendation else None
        }
    
    def notify(self):
        notif = Notification(self.reqID, self.staffID)
        db.session.add(notif)
        db.session.commit()
        return notif
    
    def set_status(self, status):        
        if self.status == Status.PENDING:
            if status in Status:
                self.status = Status(status)
                db.session.add(self)
                db.session.commit()
                return True
        return False
    
    def reject_expired_request(self):
        if (self.deadline.astimezone() < datetime.now().astimezone()) and (self.status in [Status.PENDING, Status.ACCEPTED]):
            self.status = Status.EXPIRED
            db.session.add(self)
            db.session.commit()
    
    def complete_request(self):
        if self.status == Status.ACCEPTED:
            self.status = Status.COMPLETED
            db.session.add(self)
            db.session.commit()
    
    def cancel_request(self):
        if (self.status in [Status.PENDING, Status.ACCEPTED]):
            self.status = Status.CANCELLED
            db.session.add(self)
            db.session.commit()
            return True
        return False