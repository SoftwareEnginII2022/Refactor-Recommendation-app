from flask import Blueprint, redirect, render_template, request, send_from_directory, url_for, flash
from flask_login import login_required, current_user

from App.controllers import (
    get_staff,
    get_student,
    get_staff_notifications,
    get_accepted_request_by_staffID,
    get_all_student_requests,
    get_staff_names,
)

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
def homepage():
    if not current_user:
        return render_template('index.html')
        
    userID = current_user.id
    if get_staff(userID):
        notifs = get_staff_notifications(userID)
        print(notifs)
        accepted_req_students=get_accepted_request_by_staffID(userID)
        return render_template('notif/index.html', notifs=notifs, accepted_req_students=accepted_req_students)

    elif get_student(userID):
        requests = get_all_student_requests(current_user.id)
        teachers = get_staff_names()
        return render_template('request/index.html',requests = requests, teachers = teachers)

@index_views.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')


@index_views.route('/signup', methods=['GET'])
def signup_page():
    return render_template('signup.html')
