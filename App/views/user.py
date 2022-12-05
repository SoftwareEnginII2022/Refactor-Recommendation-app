from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from App.database import db
from sqlalchemy.exc import IntegrityError

from App.controllers import (
    create_user,
    get_all_users_json,
    get_user_by_email,
)

user_views = Blueprint('user_views', __name__, template_folder='../templates')


# SIGNUP - CREATE ACCOUNT
@user_views.route('/signup', methods=['POST'])
def signup_action():
    data = request.form  # get data from form submission
    userType = data.get('userType', "User")
    if (userType != "student") and (userType != "staff"):
        flash("Please sign up as either staff or student")
        return redirect(url_for('index_views.signup_page'))

    email = data.get('email')
    password = data.get('password')
    password2 = data.get('password2')
    firstName = data.get('firstName')
    lastName = data.get('lastName')

    invalid_messages = []
    if not firstName or  (type(firstName) == str and not firstName.strip()):
        invalid_messages.append("First name cannot be blank.")
    if not lastName or  (type(lastName) == str and not lastName.strip()):
        invalid_messages.append("Last name cannot be blank.")
    if not email or  (type(email) == str and not email.strip()):
        invalid_messages.append("Please enter a valid email address.")
    if not password or  (type(password) == str and not password.strip()):
        invalid_messages.append("Please enter an appropriate password.")
    if password != password2:
        invalid_messages.append("Passowrds must match.")
    
    if invalid_messages:
        flash(" ".join(invalid_messages))
        return redirect(url_for('index_views.signup_page'))

    newuser = create_user(email, password, userType, firstName, lastName)  # create user object
    
    try:
        db.session.add(newuser)
        db.session.commit()  # save user
        login_user(newuser)  # login the user
        flash(userType.capitalize() + 'Account Created! ' + newuser.getName() + " has been logged in successfully.")  # send message
        return redirect(url_for('index_views.home_page'))  # redirect to homepage
    except IntegrityError:  # attempted to insert a duplicate user
        db.session.rollback()
        flash("Email already exists")  # error message
    return redirect(url_for('index_views.signup_page'))

# Login User
@user_views.route('/login', methods=['POST'])
def login_action():
    data = request.form
    email = data.get('email')
    password = data.get('password')

    invalid_messages = []
    if not email or  (type(email) == str and not email.strip()):
        invalid_messages.append("Please enter a valid email address.")
    if not password or  (type(password) == str and not password.strip()):
        invalid_messages.append("Please enter an appropriate password.")

    if invalid_messages:
        flash(" ".join(invalid_messages))
        return redirect(url_for('index_views.login_page'))

    user = get_user_by_email(email)
    if user and user.check_password(password):  # check credentials
        flash(user.getName() + ' has been logged in successfully.')  # send message to next page
        login_user(user)  # login the user
        return redirect(url_for('index_views.home_page'))  # redirect to main page if login successful
    else:
        flash('Invalid email or password')  # send message to next page
    return redirect(url_for('index_views.login_page'))

@user_views.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash('Logged Out!')
    return redirect(url_for('index_views.login_page')) 