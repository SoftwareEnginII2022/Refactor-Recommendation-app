from App.database import db
from datetime import date
import enum

class Status(enum.Enum):
    TRUE = "True"
    FALSE = "FALSE"

class Notification(db.Model):
    notificationID = db.Column(db.Integer, primary_key=True)
    reqID = db.Column(db.Integer, db.ForeignKey('request_recommendation.reqID'))
    staffID = db.Column(db.Integer, db.ForeignKey('staff.staffID'))
    timestamp = db.Column(db.Date, nullable= False, default= date(1970,1,1))
    seen = db.Column(db.Enum(Status), nullable=False, default=Status.FALSE)

    def __init__(self, reqID,staffID, timestamp):
        self.reqID = reqID
        self.staffID=staffID
        self.timestamp=timestamp
        self.seen =Status.FALSE
        
    def toJSON(self):
        return{
            'notificationID': self.notificationID,
            'reqID': self.reqID,
            'staffID': self.staffID,
            'deadline': self.timestamp,
            'status': self.seen
        }