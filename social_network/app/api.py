from flask import Blueprint

from app import db

api = Blueprint('api', __name__)

@api.route('/')
def main():
	return '<h1>Api</h1>'
