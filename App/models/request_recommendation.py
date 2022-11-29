from App.database import db
from datetime import date

class Request_Recommendation(db.Model):
    reqID = db.Column(db.Integer, primary_key=True)
    staffID = db.Column(db.Integer, db.ForeignKey('staff.staffID'))
    studentID = db.Column(db.Integer, db.ForeignKey('student.studentID'))
    timestamp = db.Column(db.Date, nullable= False, default= date(1970,1,1))
    requestBody = db.Column(db.String, nullable=False)
    # Recommendation = db.relationship('Recommendation', uselist=True, backref='request_recommendation', lazy=True, cascade="all, delete-orphan")

    def __init__(self, staffID, studentID, timestamp, requestBody):
        self.staffID = staffID
        self.studentID = studentID
        self.timestamp = timestamp        
        self.requestBody=requestBody

    def toJSON(self):
        return{
            'id': self.id,
            'staffID': self.staffID,
            'studentID': self.studentID,
            'timestamp': self.timestamp,
            'requestBody': self.requestBody,
            'recommendation': self.Recommendation.toJSON() if self.Recommendation else None
        }
    
    def notify():
        pass
    