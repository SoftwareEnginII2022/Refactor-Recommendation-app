from flask import Blueprint, redirect, render_template, request, send_from_directory
from flask_login import login_required, current_user

from App.controllers import (
    get_staff,
    get_staff_notification
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
    if get_staff(current_user.id):
        notifs = get_staff_notification(current_user.staffID)
        return render_template('notif/index.html', notifs=notifs)
    return render_template('index.html')