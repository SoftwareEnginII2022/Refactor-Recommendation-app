import os
from flask import Flask, flash, redirect, url_for
from flask_login import LoginManager, current_user
from flask_uploads import DOCUMENTS, IMAGES, TEXT, UploadSet, configure_uploads
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from datetime import timedelta


from App.database import create_db

from App.controllers import (
    get_user,
)

from App.views import (
    user_views,
    index_views,
    student_views,
    staff_views,
    notification_views,
    recommendation_views,
    request_reccommendation_views,
)

# New views must be imported and added to this list

views = [
    user_views,
    index_views,
    student_views,
    staff_views,
    notification_views,
    recommendation_views,
    request_reccommendation_views
]


''' Begin Flask Login Functions '''
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return get_user(user_id)


''' End Flask Login Functions '''
''' Begin boilerplate code '''

def add_views(app, views):
    for view in views:
        app.register_blueprint(view)


def invalid_route(e):
    flash("Page not found. Redirected to homepage")
    url = url_for('index_views.home_page')
    return redirect(url), 404, {"Refresh": "1; url="+ url}


def loadConfig(app, config):
    app.config['ENV'] = os.environ.get('ENV', 'DEVELOPMENT')
    delta = 7
    if app.config['ENV'] == "DEVELOPMENT":
        app.config.from_object('App.config')
        delta = app.config['JWT_EXPIRATION_DELTA']
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
        app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
        app.config['DEBUG'] = os.environ.get('ENV').upper() != 'PRODUCTION'
        app.config['ENV'] = os.environ.get('ENV')
        delta = os.environ.get('JWT_EXPIRATION_DELTA', 7)
        
    app.config['JWT_EXPIRATION_DELTA'] = timedelta(days=int(delta))
        
    for key, value in config.items():
        app.config[key] = config[key]

def create_app(config={}):
    app = Flask(__name__, static_url_path='/static')
    CORS(app)
    loadConfig(app, config)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['PREFERRED_URL_SCHEME'] = 'https'
    app.config['UPLOADED_PHOTOS_DEST'] = "App/uploads"
    photos = UploadSet('photos', TEXT + DOCUMENTS + IMAGES)
    configure_uploads(app, photos)
    add_views(app, views)
    create_db(app)
    login_manager.init_app(app)
    app.register_error_handler(404, invalid_route)
    app.app_context().push()
    return app