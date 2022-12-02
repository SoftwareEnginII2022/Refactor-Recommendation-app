from flask import Blueprint, render_template, jsonify, request, send_from_directory, Response

student_views = Blueprint('student_views', __name__, template_folder='../templates')

# students view shown on "/" when they are logged in, handled in index.py view