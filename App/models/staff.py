from App.database import db
from App.models import User

class Staff(User):
    staffID = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    Notification = db.relationship('Notification', backref='staff', lazy=True, cascade="all, delete-orphan")
    
    def toJSON(self):
        return {
            'staffID': self.staffID,
            'email': self.email,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'notifications': [notif.toJSON() for notif in self.Notification]
        }
    