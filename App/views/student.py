from flask import Blueprint, render_template, jsonify, request, send_from_directory, Response
from flask_jwt import jwt_required, current_identity

from App.controllers import (
    get_student,
    search_staff,
    get_all_students,
    get_all_students_json,
    get_student_reclist_json
)

student_views = Blueprint('student_views', __name__, template_folder='../templates')

# SEARCH STAFF
@student_views.route('/student/search', methods=['GET'])
@jwt_required()
def searchStaff():
    id = current_identity.id
    if get_student(id):
        sID = request.args.get('staffID')
        fn = request.args.get('firstName')
        ln = request.args.get('lastName')
        if (sID):
            staff=search_staff("ID", sID)
        else:
            if (fn and ln):
                staff=search_staff("name", fn + "," + ln)
            else:
                if (fn):
                    staff=search_staff("firstName", fn)
                else:
                    if(ln):
                        staff=search_staff("lastName", ln)
        if staff:
            return staff
        return Response({'staff member not found'}, status=404)
    return Response({"staff cannot perform this action"}, status=401)


# VIEW RECOMMENDATION LISTING
@student_views.route('/recommendations', methods=['GET'])
@jwt_required()
def get_recommendations():
    studentID = current_identity.id
    if get_student(studentID):
        recs = get_student_reclist_json(studentID)
        if recs:
            return jsonify(recs)
        return Response({'no recommendations found for this user'}, status=404)
    return Response("staff cannot perform this action", status=401)


# Routes for testing purposes
@student_views.route('/view/students', methods=['GET'])
def get_students_page():
    students = get_all_students()
    return render_template('users.html', users=students)

# JSON view all Students
@student_views.route('/students', methods=['GET'])
def get_students():
    students = get_all_students_json()
    return jsonify(students)
