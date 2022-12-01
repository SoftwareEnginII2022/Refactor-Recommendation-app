from App.database import db

class Recommendation(db.Model):
    recID = db.Column(db.Integer, primary_key=True)
    staffID = db.Column(db.Integer, db.ForeignKey('staff.staffID'))
    reqID = db.Column(db.Integer, db.ForeignKey('request_recommendation.reqID'))
    comments = db.Column(db.String, nullable=False)

    def __init__(self, reqID, staffID, comments):
        self.reqID=reqID
        self.staffID=staffID
        self.comments=comments
    
    def toJSON(self):
        return{
            'recID': self.recID,
            'reqID': self.reqID,
            'staffID': self.staffID,
            'comments': self.comments
        }

    
