from flask import Blueprint, request, jsonify

from app import db
from app.models import User, Post
from app.tools import auth_required

import datetime

api = Blueprint('api', __name__)

@api.route('/')
def main():
	return '<h1>Api</h1>'

@api.route('/post', methods=['POST'])
@auth_required
def create_post(user):
	data = request.get_json()
	if not data:
		return jsonify({'error': 'No post data'})
	text = data.get('text')
	if not text:
		return jsonify({'error': 'Text required'})
	creation_time = datetime.datetime.utcnow()
	new_post = Post(text=text, creation_time=creation_time, likes_amount=0, author=user)

	db.session.add(new_post)
	db.session.commit()

	return jsonify({'message': "Post created"})
