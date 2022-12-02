from datetime import datetime
from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash,redirect,url_for
from flask_jwt import jwt_required, current_identity
from flask_login import login_required, current_user

from App.controllers import (
    create_request,
    get_staff_names,
    get_student,
    get_all_student_requests
)

requestRec_views = Blueprint('requestRec_views', __name__, template_folder='../templates')

@requestRec_views.route('/requestRec/api',methods=['POST'])
@jwt_required()
def new_request_api():
    data = request.get_json()
    request = create_request(data['staffID'], current_identity.id, data['deadline'],data['requestBody'] )
    if not request:
        return jsonify({"message":"error"}),500
    return jsonify(request.toJSON()),200

@requestRec_views.route('/requestRec', methods=['GET'])
@login_required
def request_page():
    if get_student(current_user.id):
        requests = get_all_student_requests(current_user.id)
        teachers = get_staff_names()
        return render_template('requestRecommendation.html',requests = requests, teachers = teachers)
    flash("Staff cannot perform this function")
    return redirect(url_for('index_views.homepage'))

@requestRec_views.route('/requestRec',methods=['POST'])
@login_required
def new_request():
    if get_student(current_user.id):
        data = request.form
        new_request = create_request(data['staffID'], current_user.id, datetime.strptime(data['deadline'],"%Y-%m-%d"),data['requestBody'])
        if not new_request:
            flash("Error you already have a pending request to this Lecturer")
        return redirect(url_for('requestRec_views.request_page'))
    flash("Staff cannot perform this function")
    return redirect(url_for('index_views.homepage'))
