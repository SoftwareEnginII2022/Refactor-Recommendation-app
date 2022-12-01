from datetime import datetime
from flask import Blueprint, render_template, jsonify, request, send_from_directory
from datetime import datetime
from flask_login import login_required, current_user

from App.controllers import (
    create_request,
    get_all_staff,
    get_all_student_requests
)

requestRec_views = Blueprint('requestRec_views', __name__, template_folder='../templates')

# @requestRec_views.route('/requestRec/api',methods=['POST'])
# @jwt_required()
# def new_request_api():
#     data = request.get_json()
#     request = create_request(data['staffID'], current_identity.id, data['deadline'],data['requestBody'] )
#     if not request:
#         return jsonify({"message":"error"}),500
#     return jsonify(request.toJSON()),200

@requestRec_views.route('/requestRec', methods=['GET'])
@login_required
def test_page():
    requests = get_all_student_requests(current_user.id)
    teachers = get_all_staff()
    return render_template('requestRecommendation.html', requests = requests, teachers = teachers, today = datetime.today().strftime('%Y-%m-%d'))

@requestRec_views.route('/requestRec',methods=['POST'])
@login_required
def new_request_action():
    data = request.form
    new_request = create_request(data['staffID'], current_user.id, datetime.strptime(data['deadline'],"%Y-%m-%d"),data['requestBody'])
    if not new_request:
        return test_page()
    return test_page()