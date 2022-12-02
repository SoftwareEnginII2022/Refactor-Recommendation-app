from flask import Blueprint, render_template, jsonify, request, send_from_directory, Response, redirect, url_for, session, flash
from flask_login import login_required, current_user


notification_views = Blueprint('notification_views', __name__, template_folder='../templates')

# notification view shown on "/" when staff is logged in, handled in index.py view