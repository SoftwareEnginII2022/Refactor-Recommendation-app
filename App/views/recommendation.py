from flask import Blueprint, render_template, jsonify, request, send_from_directory, Response, redirect, url_for, flash
from flask_login import login_required, current_user

from App.controllers import (
    get_recommendation,
    get_all_recommendations_json,
    get_student,
    get_staff,
    get_recommendation,
    get_student_request_json,
    create_recommendation
)

recommendation_views = Blueprint('recommendation_views', __name__, template_folder='../templates')

# Route for creating a recommendation with a valid request
@recommendation_views.route('/recommendation', methods=['POST'])
@login_required
def create_recommendation_action():
    if not get_staff(current_user.id):
        return redirect(url_for("index_views.homepage"))
    data = request.form
    nones = ["-1"] * 2
    reqDetails = data.get("reqDetails", "-1,")
    [reqID, studentName, *z] = reqDetails.split(",") + nones

    print(reqID)
    print(studentName)
    print(reqDetails)
    print(data['comments'])

    created_rec = create_recommendation(reqID, current_user.id, data['comments'])
    
    if created_rec:
        flash("Recommendation successfully created for " + studentName)
    else:
        flash("Could not create recommendation for.")

    return redirect(url_for("index_views.homepage"))

# Route for viewing individual recommendations
@recommendation_views.route('/recommendation/<recID>', methods=['GET'])
@login_required
def get_recommendation_action(recID):
    if not get_student(current_user.id):
        flash("You cannot view that page.")
        return redirect(url_for("index_views.homepage"))

    recommendation = get_recommendation(recID)

    return render_template('recommendation/view.html', recommendation=recommendation)
