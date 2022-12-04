from datetime import datetime
from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash,redirect,url_for, session
from flask_login import login_required, current_user

from App.controllers import (
    create_request,
    get_student,
    get_recommendation_by_request,
    set_notification_seen,
    get_staff,
    accept_request,
    reject_request,
    cancel_request,
    get_notification_by_request
)

request_reccommendation_views = Blueprint('request_reccommendation_views', __name__, template_folder='../templates')


# View notification by ID
@request_reccommendation_views.route('/recommendation_request/<reqID>', methods=['GET'])
@login_required
def view_notif(reqID):
    if get_staff(current_user.id):
        notif = get_notification_by_request(reqID)
        notif = set_notification_seen(notif)
        recommendation = get_recommendation_by_request(reqID)
        session['notif_url'] = url_for('request_reccommendation_views.view_notif', reqID=reqID)
        return render_template('request/view.html', notif=notif, recommendation=recommendation)
    flash("You cannot view that page.")
    return redirect(url_for('index_views.home_page'))


# Accept request by ID
@request_reccommendation_views.route('/recommendation_request/<reqID>/accept', methods=['GET'])
@login_required
def accept_request_action(reqID):
    if get_staff(current_user.id):
        if not accept_request(reqID):
            flash("Recommendation request could not be accepted")
        else:
            flash("Recommendation request accepted")
        return redirect(session.get('notif_url', url_for('index_views.home_page')))
    flash("You cannot perform this action")
    return redirect(url_for('index_views.home_page'))

# Reject request by ID
@request_reccommendation_views.route('/recommendation_request/<reqID>/reject', methods=['GET'])
@login_required
def reject_request_action(reqID):
    if get_staff(current_user.id):
        if not reject_request(reqID):
            flash("Recommendation request coult not be rejected")
        else:
            flash("Recommendation request rejected")
            
        if 'notif_url' in session:
            return redirect(session['notif_url'])
        else:
            return redirect(url_for('index_views.home_page'))
    flash("You cannot perform this action")
    return redirect(url_for('index_views.home_page'))

# Cancel request by ID
@request_reccommendation_views.route('/recommendation_request/<reqID>/cancel', methods=['GET'])
@login_required
def cancel_request_action(reqID):
    if get_student(current_user.id):
        if not cancel_request(reqID):
            flash("Recommendation request coult not be cancelled")
        else:
            flash("Recommendation request cancelled")
            
        return redirect(url_for('index_views.home_page'))

    flash("You cannot perform this action")
    return redirect(url_for('index_views.home_page'))

@request_reccommendation_views.route('/recommendation_request', methods=['POST'])
@login_required
def new_request():
    if not get_student(current_user.id):
        flash("Staff cannot perform this function")
        return redirect(url_for('index_views.home_page'))

    data = request.form
    staffID = data.get('staffID')
    deadline = validate_date(data.get('deadline'))
    requestBody = data.get('requestBody')

    invalid_messages = []
    if not staffID:
        invalid_messages.append("Please select valid lecturer.")
    if not deadline:
        invalid_messages.append("Please choose valid date.")
    elif deadline < datetime.today():
        invalid_messages.append("Please choose future deadline date.")
    if not requestBody or  (type(requestBody) == str and not requestBody.strip()):
        invalid_messages.append("Please enter a description for your recommendation request. Blank descriptions are more likely to get declined.")
    
    if invalid_messages:
        flash(" ".join(invalid_messages))
        return redirect(url_for('index_views.home_page'))

    new_request = create_request(staffID, current_user.id, deadline, requestBody)
    if not new_request:
        flash("You already have a pending request for this Lecturer. Please wait until it has been Completed, Rejected, or Expired, before sending another request.")
    else:
        flash("Recommendation request created. The Lecturer will be notified")

    return redirect(url_for('index_views.home_page'))
    

def validate_date(date_text):
    try:
        return datetime.strptime(date_text, '%Y-%m-%d')
    except:
        return None