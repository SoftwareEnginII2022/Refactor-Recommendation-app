from flask import Blueprint, redirect, render_template, request, send_from_directory, url_for, flash, session
from datetime import datetime, timedelta
from flask_login import login_required, current_user

from App.controllers import (
    get_staff,
    get_student,
    get_staff_notifications,
    get_accepted_request_by_staffID,
    get_student_requests,
    get_staff_names,
)

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
def home_page():
    if not current_user or not current_user.is_authenticated:
        return render_template('index.html')
        
    userID = current_user.id
    if get_staff(userID):
        notifs = get_staff_notifications(userID)
        accepted_req_students=get_accepted_request_by_staffID(userID)
        session['notif_url'] = url_for('index_views.home_page')
        return render_template('notif/index.html', notifs=notifs, accepted_req_students=accepted_req_students)

    elif get_student(userID):
        requests = get_student_requests(userID)
        teachers = get_staff_names()
        return render_template('request/index.html',requests = requests, teachers = teachers, today = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d'))

@index_views.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')


@index_views.route('/signup', methods=['GET'])
def signup_page():
    return render_template('signup.html')
