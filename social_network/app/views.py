from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

import datetime

from app import db
from app.models import User, Post

auth = Blueprint('auth', __name__)

@auth.route('/singup', methods=['POST'])
def singup():
	data = request.get_json()
	name = data.get('name')
	password = data.get('password')

	if not name or not password:
		return jsonify({'error': 'Name and password required'}), 400
	
	user = User.query.filter_by(name=name).first()
	if user:
		return jsonify({'error': 'This username is already taken'}), 400
	
	if len(password) < 7:
		return jsonify({'error': 'Password must be at least 7 characters'}), 400
	
	creation_time = datetime.datetime.utcnow()
	hashed_password = generate_password_hash(password, method='sha256')
	new_user = User(name=name, password=hashed_password, last_activity=creation_time)

	db.session.add(new_user)
	db.session.commit()

	return jsonify({'message': 'User created'})

@auth.route('/login')
def login():
	return ''