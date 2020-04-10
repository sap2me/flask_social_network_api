from flask import request, jsonify, current_app

import jwt

from app.models import User

def auth_required(func):
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
		return func(user, *args, **kwargs)
	return wrapper
