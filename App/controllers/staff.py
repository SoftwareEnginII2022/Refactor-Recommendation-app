import select
from App.models import Staff
from App.database import db
from flask import jsonify

def get_staff(id):
    staff=Staff.query.get(id)
    if staff:
        return staff
    return None
    
def get_staff_names():
    staff = db.session.execute(db.select(Staff.staffID,Staff.firstName, Staff.lastName)).all()

    if not staff:
       return None
    return staff

def get_staff_notification_feed(staffID):
    staff = get_staff(staffID)
    return staff.Notification