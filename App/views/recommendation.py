from flask import Blueprint, render_template, jsonify, request, send_from_directory, Response, redirect, url_for, flash, session
from flask_login import login_required, current_user

from App.controllers import (
    get_recommendation,
    get_student,
    get_staff,
    create_recommendation
)

recommendation_views = Blueprint('recommendation_views', __name__, template_folder='../templates')

# Route for viewing individual recommendations
@recommendation_views.route('/recommendation/<recID>', methods=['GET'])
@login_required
def get_recommendation_action(recID):
    if not get_student(current_user.id):
        flash("You cannot view that page.")
        return redirect(url_for("index_views.home_page"))

    recommendation = get_recommendation(recID)

    if not recommendation:
        flash("No recommendation found")
        return redirect(url_for("index_views.home_page"))

    return render_template('recommendation/view.html', recommendation=recommendation)

# Route for creating a recommendation with a valid request
@recommendation_views.route('/recommendation', methods=['POST'])
@login_required
def create_recommendation_action():
    if not get_staff(current_user.id):
        flash("Student cannot perform this function")
        return redirect(url_for("index_views.home_page"))

    data = request.form
    nones = ["-1"] * 2
    reqDetails = data.get("reqDetails", "-1,")
    [reqID, studentName, *z] = reqDetails.split(",") + nones
    comments = data.get('comments')

    invalid_messages = []
    if not reqID or not studentName:
        invalid_messages.append("Please select valid student.")
    if not comments or  (type(comments) == str and not comments.strip()):
        invalid_messages.append("Please enter an appropriate comment for your student's recommendation. Blank recommendations are less likely to be considered.")
    
    if invalid_messages:
        flash(" ".join(invalid_messages))
        return redirect(session.get('notif_url', url_for('index_views.home_page')))

    created_rec = create_recommendation(reqID, current_user.id, comments)
    
    if created_rec:
        flash("Recommendation successfully created for " + studentName)
    else:
        flash("Could not create recommendation.")

    return redirect(url_for("index_views.home_page"))