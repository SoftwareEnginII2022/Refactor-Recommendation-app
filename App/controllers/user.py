from App.models import User, Student, Staff
from App.database import db
from sqlalchemy.exc import SQLAlchemyError
from flask import Response

# Create new User
def create_user(email, password, userType, firstName, lastName):
    try:
        if (userType=="student"):
            newuser = Student(email=email, password=password, firstName=firstName, lastName=lastName)
        elif (userType=="staff"):
            newuser = Staff(email=email, password=password, firstName=firstName, lastName=lastName)
        else:
            newuser = User(email=email, password=password, firstName=firstName, lastName=lastName)

        db.session.add(newuser)
        db.session.commit()
        return newuser
    except SQLAlchemyError:
        db.session.rollback()
        return None


# get User by id
def get_user(id):
    user = Student.query.get(id)
    if not user:
        user = Staff.query.get(id)
    if not user:
        user = User.query.get(id)
    return user

# get User by email
def get_user_by_email(email):
    return User.query.filter_by(email=email).first()

# get all User objects
def get_all_users():
    return User.query.all()

def get_all_users_json():
    users = User.query.all()
    if not users:
        return None
    users = [user.toJSON() for user in users]
    return users
