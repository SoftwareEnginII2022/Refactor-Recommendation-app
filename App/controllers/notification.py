from App.models import Notification
from App.database import db
from sqlalchemy.exc import IntegrityError
from App.controllers import get_staff

def create_notification(reqID,staffID,deadline):
    newNotif = Notification(reqID=reqID,staffID=staffID, timestamp=deadline)
    return newNotif

def send_notification(reqID, deadline, staffID):
    # get staff feed - notif list
    staff = get_staff(staffID)
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

# gets a notification from a user's notif feed
def get_user_notif(staffID, notifID):
    return Notification.query.filter_by(sentToStaffID=staffID, notifID=notifID).first()

def change_status(notif, status):
    if notif:
        notif.status = status
    return notif

# approve notif
def approve_notif(staffID, notifID, status):
    notif = get_user_notif(staffID, notifID)
    notif = change_status(notif, status)
    if notif:
        try:
            db.session.add(notif)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return None
    return notif
    