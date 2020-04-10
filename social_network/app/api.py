from flask import Blueprint

from app import db
from app.models import User, Post
from app.tools import auth_required

api = Blueprint('api', __name__)

@api.route('/')
def main():
	return '<h1>Api</h1>'

@api.route('/post', methods=['POST'])
@auth_required
def create_post(user):
	return 'Here'
