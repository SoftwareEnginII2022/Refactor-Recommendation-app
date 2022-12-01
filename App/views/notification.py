from flask import Blueprint, render_template, jsonify, request, send_from_directory, Response, redirect, url_for
from flask_login import login_required, current_user

from App.controllers import (
    set_notification_seen,
    send_notification,
    get_all_notifs_json,
    get_staff,
    # approve_notif,
    get_notification
)

notification_views = Blueprint('notification_views', __name__, template_folder='../templates')

# View notification by ID
@notification_views.route('/notification/<notificationID>', methods=['GET'])
@login_required
def view_notif(notificationID):
    if get_staff(current_user.id):
        notif = get_notification(notificationID)
        notif = set_notification_seen(notif)
        return render_template('notif/view.html', notif=notif)
    return redirect(url_for('index_views.homepage'))

# SEND REQUEST TO STAFF MEMBER
# @notification_views.route('/request/send', methods=['POST'])
# @jwt_required()
# def sendRequest():
#     if not get_staff(current_identity.id):
#         data = request.get_json()
#         staff = get_staff(data['sentToStaffID'])
#         if not staff:
#             return Response({'staff member not found'}, status=404)
#         send_notification(current_identity.id, data['requestBody'], data['sentToStaffID'])
#         return Response({'request sent successfully'}, status=200)
#     return Response({"staff cannot perform this action"}, status=401)


# # VIEW NOTIFICATION
# @notification_views.route('/notifications/<notifID>', methods=['GET'])
# @jwt_required()
# def view_notif(notifID):
#     staff = get_staff(current_identity.id)
#     if staff:
#         if not staff.notificationFeed:
#             return Response({"no notifications found for this user"}, status=404)
#         notif = get_user_notif(current_identity.id, notifID)
#         if notif:
#             return jsonify(notif.toJSON())
#         return Response({"notification with id " + notifID + " not found"}, status=404)
#     return Response({"students cannot perform this action"}, status=401)


# APPROVE REQUEST
# @notification_views.route('/request/<notifID>', methods=['POST'])
# @jwt_required()
# def approve_request(notifID):
#     status = request.get_json()
#     staff = get_staff(current_identity.id)
#     if staff:
#         notif = approve_notif(staff.staffID, notifID, status['status'])
#         if notif:
#             return Response({"request " + status['status']}, status=200)
#         return Response({"invalid request"}, status=401)
#     return Response({"students cannot perform this action"}, status=401)


# Routes for testing purposes

# get all notification objects
@notification_views.route('/notifs', methods=['GET'])
def get_all_notifications():
    notifs = get_all_notifs_json()
    return jsonify(notifs)