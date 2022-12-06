import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from datetime import datetime, timedelta
from App.database import db, create_db, get_migrate
from sqlalchemy.exc import IntegrityError
from App.main import create_app
from App.controllers import (
    create_request,
    create_user,
    get_all_users_json,
    get_all_users
)

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def initialize():
    create_db(app)
    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("email", default="rob@mail.com")
@click.argument("password", default="robpass")
@click.argument("userType", default="student")
@click.argument("firstName", default="Rob")
@click.argument("lastName", default="Jones")
def create_user_command(email, password, userType, firstName, lastName):
    create_user(email, password, userType, firstName, lastName)
    print(f'{firstName} {lastName} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli


'''
Generic Commands
'''

@app.cli.command("init")
def initialize():
    create_db(app)
    print('database intialized')

@app.cli.command("mockup_rec_req")
def mockup_reccommendation_request():
    student1 = create_user("student1@email.com", "student1", "student", "Stu", "Dent1")
    student2 = create_user("student2@email.com", "student2", "student", "Stu", "Dent2")
    student3 = create_user("student3@email.com", "student2", "student", "Stu", "Dent3")
    student4 = create_user("student4@email.com", "student4", "student", "Stu", "Dent4")
    student5 = create_user("student5@email.com", "student5", "student", "Stu", "Dent5")
    student6 = create_user("student6@email.com", "student6", "student", "Stu", "Dent6")
    staff1 = create_user("staff1@email.com", "staff1", "staff", "Sta", "Aff1")
    staff2 = create_user("staff2@email.com", "staff2", "staff", "Sta", "Aff2")
    staff3 = create_user("staff3@email.com", "staff3", "staff", "Sta", "Aff3")
    staff4 = create_user("staff4@email.com", "staff4", "staff", "Sta", "Aff4")
    
    try:
        db.session.add(student1)
        db.session.add(staff3)
        db.session.add(student6)
        db.session.add(student2)
        db.session.add(student5)
        db.session.add(staff2)
        db.session.add(student3)
        db.session.add(staff4)
        db.session.add(student4)
        db.session.add(staff1)
        db.session.commit()
    except IntegrityError as e:
        print("Creation failed: " + e)
        db.session.rollback()


    create_request(staff2.staffID, student4.studentID, datetime.now() - timedelta(days=5), "Student 4 to staff 2!")
    create_request(staff1.staffID, student3.studentID, datetime.now() + timedelta(days=2), "Student 3 to staff 1!")
    create_request(staff1.staffID, student4.studentID, datetime.now() + timedelta(days=4), "Student 4 to staff 1!")
    create_request(staff3.staffID, student1.studentID, datetime.now() - timedelta(days=12), "Student 1 to staff 3!")
    create_request(staff1.staffID, student6.studentID, datetime.now() + timedelta(days=3), "Student 6 to staff 1!")
    create_request(staff3.staffID, student6.studentID, datetime.now() + timedelta(days=5), "Student 6 to staff 3!")
    create_request(staff1.staffID, student1.studentID, datetime.now() - timedelta(days=7), "Student 1 to staff 1!")
    create_request(staff1.staffID, student5.studentID, datetime.now() + timedelta(days=3), "Student 5 to staff 1!")
    create_request(staff2.staffID, student1.studentID, datetime.now() - timedelta(days=2), "Student 1 to staff 2!")
    create_request(staff1.staffID, student2.studentID, datetime.now() + timedelta(days=8), "Student 2 to staff 1!")
    create_request(staff4.staffID, student5.studentID, datetime.now() + timedelta(days=6), "Student 5 to staff 4!")
    create_request(staff3.staffID, student2.studentID, datetime.now() + timedelta(days=1), "Student 2 to staff 3!")


    

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("student", help="Run Student tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "StudentUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "StudentIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "Student"]))

@test.command("staff", help="Run Staff tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "StaffUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "StaffIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "Staff"]))

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "User"]))

@test.command("req_rec", help="Run Request Recommendation tests")
@click.argument("type", default="all")
def req_rec_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "Request_RecommendationUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "Request_RecommendationIntegrationTests"]))
    else:
       sys.exit(pytest.main(["-k", "Request_Recommendation"]))

@test.command("recommend", help="Run all Recommendation test")
@click.argument("type", default="all")
def recommend_test_commands(type):
    if type == "unit":
         sys.exit(pytest.main(["-k", "RecommendationUnitTests and not Request"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "RecommendationIntegrationTests and not Request"]))
    else:
        sys.exit(pytest.main(["-k", "Recommendation and not Request"]))

@test.command("notification", help="Run Request Recommendation tests")
@click.argument("type", default="all")
def notification_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "NotificationUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "NotificationIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "Notification"]))
    

app.cli.add_command(test)