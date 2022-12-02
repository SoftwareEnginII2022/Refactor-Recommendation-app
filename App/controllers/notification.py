from App.models import Notification, Request_Recommendation
from App.database import db
from sqlalchemy.exc import IntegrityError
from App.controllers import get_user
from datetime import datetime

def create_notification(reqID,staffID,deadline):
    newNotif = Notification(reqID=reqID,staffID=staffID, timestamp=deadline)
    return newNotif

def populate_notification(notif):
    notif.Student = get_user(notif.Request_Recommendation.studentID)
    return notif

def check_expired_requests():
    req_recs = Request_Recommendation.query.filter(Request_Recommendation.deadline < datetime.today()).all()

    for req_rec in req_recs:
        req_rec.reject_expired_request()

# gets a notification from a user's notif feed
def get_staff_notifications(staffID):
    check_expired_requests()
    notifs = Notification.query.filter_by(staffID=staffID).all()

    for notif in notifs:
        notif = populate_notification(notif)
    
    return notifs

# gets a notification from a user's notif feed
def get_notification_by_request(reqID):
    check_expired_requests()
    notif = Notification.query.filter_by(reqID=reqID).first()
    notif = populate_notification(notif)

    return notif

def set_notification_seen(notif):
    notif.seen = True
    try:
        db.session.add(notif)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
    return notif
