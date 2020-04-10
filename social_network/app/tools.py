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
			return json_response('No post data', 400)
		token = data.get('jwt')
		if not token:
			return json_response('Token is missing', 400)
		try:
			data = jwt.decode(token, current_app.config['SECRET_KEY'])
			user = User.query.filter_by(name=data.get('name')).first()
			if not user:
				return json_response('There is no this user in database', 500)
		except:
			return json_response('Token is invalid', 400)
		user.last_activity = datetime.datetime.utcnow()
		db.session.commit()
		return func(user, *args, **kwargs)
	return wrapper

def json_response(message, http_code=200):
	if http_code >= 400:
		success = False
	else:
		success = True
	return jsonify({'message': message, 'success': success}), http_code