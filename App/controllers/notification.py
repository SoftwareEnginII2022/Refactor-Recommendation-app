from App.models import Notification, Request_Recommendation
from App.database import db
from sqlalchemy.exc import IntegrityError
from App.controllers import get_user
from datetime import datetime

def create_notification(reqID,staffID,deadline):
    newNotif = Notification(reqID=reqID,staffID=staffID, timestamp=deadline)
    return newNotif

def send_notification(reqID, deadline, staffID):
    # get staff feed - notif list
    staff = get_user(staffID)
    # new notif
    newNotif = create_notification(staffID, reqID, deadline)
    try:
        db.session.add(newNotif)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return None
        
    # Should not need to append this, as the relationship will have it here already
    # add notif to list
    # staff.Notification.append(newNotif)
    # try:
    #     db.session.add(staff)
    #     db.session.commit()
    # except IntegrityError:
    #     db.session.rollback()
    #     return None
    # return staff

def get_all_notifs():
    return Notification.query.all()

def get_all_notifs_json():
    notifs = get_all_notifs()
    if not notifs:
        return None
    notifs = [notif.toJSON() for notif in notifs]
    return notifs

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
def get_notification(notifID):
    check_expired_requests()
    notif = Notification.query.get(notifID)
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

# # approve notif
# def approve_notif(staffID, notifID, status):
#     notif = get_notification(notifID)
#     notif = change_status(notif, status)
#     if notif:
#         try:
#             db.session.add(notif)
#             db.session.commit()
#         except IntegrityError:
#             db.session.rollback()
#             return None
#     return notif
    