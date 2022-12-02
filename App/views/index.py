from flask import Blueprint, redirect, render_template, request, send_from_directory, url_for
from flask_login import login_required, current_user

from App.controllers import (
    get_staff,
    get_student,
    get_staff_notifications,
    get_accepted_request_by_staffID
)

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
def index_page():
    return render_template('index.html')

@index_views.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')


@index_views.route('/signup', methods=['GET'])
def signup_page():
    return render_template('signup.html')
    
@index_views.route('/app', methods=['GET'])
@login_required
def homepage():
    userID = current_user.id
    if get_staff(userID):
        notifs = get_staff_notifications(userID)
        accepted_req_students=get_accepted_request_by_staffID(userID)
        return render_template('notif/index.html', notifs=notifs, accepted_req_students=accepted_req_students)
    if get_student(userID):
        return redirect(url_for('requestRec_views.request_page'))
    return render_template('index.html')