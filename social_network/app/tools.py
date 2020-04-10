from flask import request, jsonify, current_app

from functools import wraps
import datetime

import jwt

from app import db
from app.models import User

def auth_required(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		data = request.get_json()
		if not data:
			return jsonify({'error': 'No post data'})
		token = data.get('jwt')
		if not token:
			return jsonify({'error': 'Token is missing'})
		try:
			data = jwt.decode(token, current_app.config['SECRET_KEY'])
			user = User.query.filter_by(name=data.get('name')).first()
			if not user:
				return jsonify({'error': 'There is no this user in database'}), 500
		except:
			return jsonify({'error': 'Token is invalid'}), 401
		user.last_activity = datetime.datetime.utcnow()
		db.session.commit()
		return func(user, *args, **kwargs)
	return wrapper
