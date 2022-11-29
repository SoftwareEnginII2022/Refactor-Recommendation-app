from App.database import db
from datetime import date
import enum

class Status(enum.Enum):
    READ = "Read"
    UNREAD = "Unread"
    COMPLETED = "Completed"

class Notification(db.Model):
    notificationID = db.Column(db.Integer, primary_key=True)
    reqID = db.Column(db.Integer, db.ForeignKey('Request_Recommendation.reqID'))
    staffID = db.Column(db.Integer, db.ForeignKey('staff.staffID'))
    deadline = db.Column(db.Date, nullable= False, default= date(1970,1,1))
    status = db.Column(db.Enum(Status), nullable=False, default=Status.UNREAD)

    def __init__(self, reqID,staffID, deadline):
        self.reqID = reqID
        self.staffID=staffID
        self.deadline=deadline
        self.status=Status.UNREAD
        
    def toJSON(self):
        return{
            'notificationID': self.notificationID,
            'reqID': self.reqID,
            'staffID': self.staffID,
            'deadline': self.deadline,
            'status': self.status
        }