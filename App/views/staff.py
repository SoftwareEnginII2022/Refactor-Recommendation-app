from flask import Blueprint, render_template, jsonify, request, send_from_directory, Response

staff_views = Blueprint('staff_views', __name__, template_folder='../templates')


# staff view shown on "/" when they are logged in, handled in index.py view