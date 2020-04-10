from flask import Blueprint

from app import db

auth = Blueprint('auth', __name__)

@auth.route('/singup')
def singup():
	return ''

@auth.route('/login')
def login():
	return ''