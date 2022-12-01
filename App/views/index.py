from flask import Blueprint, redirect, render_template, request, send_from_directory
from flask_login import LoginManager, login_required

from App.controllers import (
    get_user,
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

@index_views.route('/request', methods=['GET'])
def test_page():
    return render_template('requestRecommendation.html')
    
@index_views.route('/app', methods=['GET'])
@login_required
def login_required():
    return render_template('index.html')
#   todos = todos = Todo.query.filter_by(userid=current_user.id).all()
#   return render_template('todo.html', todos=todos)