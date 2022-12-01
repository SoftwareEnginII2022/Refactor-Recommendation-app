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
    staff = create_user("staff@email.com", "staff", "staff", "St", "Aff")
    
    try:
        db.session.add(student1)
        db.session.add(student2)
        db.session.add(student3)
        db.session.add(staff)
        db.session.commit()
    except IntegrityError as e:
        print("Creation failed: " + e)
        db.session.rollback()

    rec_req1 = create_request(staff.staffID, student1.studentID, datetime.now() + timedelta(days=7), "Hi, I am a student 1. Please send me a recommendation 1!")
    rec_req2 = create_request(staff.staffID, student2.studentID, datetime.now() - timedelta(days=7), "Hi, I am a student 2. Please send me a recommendation 2!")
    rec_req3 = create_request(staff.staffID, student3.studentID, datetime.now() + timedelta(days=2), "Hi, I am a student 3. Please send me a recommendation 3!")
    db.session.add(rec_req1)
    db.session.add(rec_req2)
    db.session.add(rec_req3)
    db.session.commit()

    rec_req1.notify()
    rec_req2.notify()
    rec_req3.notify()

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)