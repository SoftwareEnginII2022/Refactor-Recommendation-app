from App.database import db
from App.models import User

class Student(User):
    studentID = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    Requests = db.relationship('Request_Recommendation', backref='student', lazy=True, cascade="all, delete-orphan")
    
    def toJSON(self):
        return {
            'studentID': self.studentID,
            'email': self.email,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'requests': [req.toJSON() for req in self.Requests]
        }
    
    def getType(self):
        return "student"