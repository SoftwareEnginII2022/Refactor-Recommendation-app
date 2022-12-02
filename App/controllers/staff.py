import select
from App.models import Staff
from App.database import db
from flask import jsonify

def get_staff(id):
    staff=Staff.query.get(id)
    if staff:
        return staff
    return None

def get_all_staff():
    return Staff.query.all()

def get_all_staff_json():
    staff = get_all_staff()
    if not staff:
        return None
    staff = [staf.toJSON() for staf in staff]
    return staff

def get_all_staff_notifs_json():
    staff = get_all_staff()
    if not staff:
        return None
    staff = [staf.toJSON() for staf in staff]
    return staff

def get_staff_by_firstName(firstName):
    staff= Staff.query.filter_by(firstName=firstName).all()
    staff = [staf.toJSON() for staf in staff]
    if staff==[]:
        return None
    return jsonify(staff)

def get_staff_by_lastName(lastName):
    staff=Staff.query.filter_by(lastName=lastName).all()
    staff = [staf.toJSON() for staf in staff]
    if not staff:
        return None
    return jsonify(staff)

def get_staff_by_name(firstName, lastName):
    staff=Staff.query.filter_by(firstName=firstName, lastName=lastName).all()
    staff = [staf.toJSON() for staf in staff]
    if not staff:
        return None
    return jsonify(staff)
    
def get_staff_names():
    staff = db.session.execute(db.select(Staff.staffID,Staff.firstName, Staff.lastName)).all()

    if not staff:
       return None
    return staff

def search_staff(type, keyword):
    if (type=="ID"):
        staff = get_staff(keyword)
        return staff.toJSON()
    elif (type=="name"):
        name=keyword.split(",")
        return get_staff_by_name(name[0], name[1])
    elif (type=="firstName"):
        return get_staff_by_firstName(keyword)
    elif (type=="lastName"):
        return get_staff_by_lastName(keyword)
    return None

def get_staff_notification_feed(staffID):
    staff = get_staff(staffID)
    return staff.Notification

# get the notification feed for the current user
def get_staff_notification_feed_json(staffID):
    notifs = get_staff_notification_feed(staffID)
    if notifs:
        return [notif.toJSON() for notif in notifs]
    return None

