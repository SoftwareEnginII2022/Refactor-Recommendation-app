from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt import jwt_required, current_identity
from flask_login import login_user, login_required, logout_user
from App.database import db
from sqlalchemy.exc import IntegrityError

from App.controllers import (
    create_user,
    get_all_users,
    get_all_users_json,
    get_user,
    get_all_requests_json,
    get_user_by_email,
)

user_views = Blueprint('user_views', __name__, template_folder='../templates')


# SIGNUP - CREATE ACCOUNT
@user_views.route('/signup', methods=['POST'])
def signupAction():
    data = request.form  # get data from form submission
    if (data['userType'] == "student") or (data['userType'] == "staff"):
        newuser = create_user(data['email'],
            data['password'],
            data['userType'],
            data['firstName'],
            data['lastName'])  # create user object
    else:
        flash("Invalid account type: " + data['userType'])
        return redirect(url_for('index_views.signup_page'))
    
    try:
        db.session.add(newuser)
        db.session.commit()  # save user
        login_user(newuser)  # login the user
        flash(data['userType'].capitalize() + 'Account Created!')  # send message
        return redirect('/app')  # redirect to homepage
    except IntegrityError:  # attempted to insert a duplicate user
        db.session.rollback()
        flash("Email already exists")  # error message
    return redirect(url_for('index_views.signup_page'))

# Login User
@user_views.route('/login', methods=['POST'])
def loginAction():
    data = request.form
    user = get_user_by_email(data['email'])
    if user and user.check_password(data['password']):  # check credentials
        flash('Logged in successfully.')  # send message to next page
        login_user(user)  # login the user
        return redirect('/app')  # redirect to main page if login successful
    else:
        flash('Invalid email or password')  # send message to next page
    return redirect(url_for('index_views.login_page'))

@user_views.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash('Logged Out!')
    return redirect(url_for('index_views.login_page')) 


# Routes for testing purposes
# check identity of current user
@user_views.route('/identify', methods=['GET'])
@jwt_required()
def identify_user_action():
    return jsonify({'message': f"id : {current_identity.id}, email: {current_identity.email}, userType: {current_identity.userType}"})

# View all Users
@user_views.route('/view/users', methods=['GET'])
def get_user_page():
    users = get_all_users()
    return render_template('users.html', users=users)

# JSON View all Users
@user_views.route('/users')
def client_app():
    users = get_all_users_json()
    return jsonify(users)

# STATIC View all Users
@user_views.route('/static/users', methods=['GET'])
def static_user_page():
  return send_from_directory('static/user', 'index.html')


# JSON View all Users
@user_views.route('/requests')
def client_app_requests():
    requests = get_all_requests_json()
    print(requests)
    return jsonify(requests)

# STATIC View all Requests
@user_views.route('/static/requests', methods=['GET'])
def static_user_page_requests():
  return send_from_directory('static/request', 'index.html')