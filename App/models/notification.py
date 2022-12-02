from App.database import db
from datetime import datetime
from sqlalchemy.sql import func


class Notification(db.Model):
    notificationID = db.Column(db.Integer, primary_key=True)
    reqID = db.Column(db.Integer, db.ForeignKey('request_recommendation.reqID'))
    staffID = db.Column(db.Integer, db.ForeignKey('staff.staffID'))
    timestamp = db.Column(db.DateTime(timezone=True), nullable= False, default=func.now())
    seen = db.Column(db.Boolean, nullable=False, default=False)
    Request_Recommendation = db.relationship('Request_Recommendation', single_parent=True, uselist=False, backref='notification', lazy=True, cascade="all, delete-orphan")

    def __init__(self, reqID,staffID):
        self.reqID = reqID
        self.staffID=staffID
        self.timestamp=datetime.today()
        self.seen=False
        
    def toJSON(self):
        return{
            'notificationID': self.notificationID,
            'reqID': self.reqID,
            'staffID': self.staffID,
            'timestamp': self.timestamp,
            'request': self.Request_Recommendation.toJSON() if self.Request_Recommendation else None,
            'seen': self.seen
        }