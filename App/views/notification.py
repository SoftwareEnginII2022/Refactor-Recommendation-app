from flask import Blueprint, render_template, jsonify, request, send_from_directory, Response, redirect, url_for, session, flash
from flask_login import login_required, current_user

from App.controllers import (
    set_notification_seen,
    get_staff,
    accept_request,
    reject_request,
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
        session['notif_url'] = url_for('notification_views.view_notif', notificationID=notificationID)
        return render_template('notif/view.html', notif=notif)
    flash("You cannot view that page.")
    return redirect(url_for('index_views.homepage'))


# Accept request by ID
@notification_views.route('/request/<reqID>/accept', methods=['GET'])
@login_required
def accept_request_action(reqID):
    if get_staff(current_user.id):
        accept_request(reqID)
        flash("Recommendation request accepted")
        if 'notif_url' in session:
            return redirect(session['notif_url'])
        else:
            return redirect(url_for('index_views.homepage'))
    flash("You cannot perform this action")
    return redirect(url_for('index_views.homepage'))

# Reject request by ID
@notification_views.route('/request/<reqID>/reject', methods=['GET'])
@login_required
def reject_request_action(reqID):
    if get_staff(current_user.id):
        reject_request(reqID)
        flash("Recommendation request rejected")
        if 'notif_url' in session:
            return redirect(session['notif_url'])
        else:
            return redirect(url_for('index_views.homepage'))
    flash("You cannot perform this action")
    return redirect(url_for('index_views.homepage'))