from datetime import datetime
from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash,redirect,url_for
from flask_jwt import jwt_required, current_identity
from flask_login import login_required, current_user

from App.controllers import (
    create_request,
    get_student,
)

request_reccommendation_views = Blueprint('request_reccommendation_views', __name__, template_folder='../templates')


@request_reccommendation_views.route('/recommendation_request', methods=['POST'])
@login_required
def new_request():
    if get_student(current_user.id):
        data = request.form
        new_request = create_request(data['staffID'], current_user.id, datetime.strptime(data['deadline'],"%Y-%m-%d"),data['requestBody'])
        if not new_request:
            flash("You already have a pending request to this Lecturer")
        else:
            flash("Recommendation request created. The Lecturer will be notified")
        return redirect(url_for('index_views.homepage'))
    flash("Staff cannot perform this function")
    return redirect(url_for('index_views.homepage'))
