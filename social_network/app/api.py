from flask import Blueprint, request, jsonify

from app import db
from app.models import User, Post
from app.tools import auth_required, json_response

import datetime

api = Blueprint('api', __name__)

@api.route('/')
def main():
	return '<h1>Api</h1>'

@api.route('/post', methods=['POST'])
@auth_required
def create_post(user):
	""" Create new post """
	data = request.get_json()
	text = data.get('text')
	if not text:
		return jsonify({'error': 'text is missing'})
	creation_time = datetime.datetime.utcnow()
	new_post = Post(text=text, creation_time=creation_time, likes_amount=0, author=user)

	db.session.add(new_post)
	db.session.commit()

	return jsonify({'message': "Post created"})

@api.route('/post/like', methods=['POST'])
@auth_required
def like_post(user):
	""" Like post """
	data = request.get_json()
	post_id = data.get('post_id')
	if not post_id:
		return jsonify({'error': "post_id is missing"})
	post = Post.query.filter_by(id=int(post_id)).first()
	if not post:
		return jsonify({'error': "post_id is incorrect"})
	if user in post.user_likes:
		return jsonify({'error': "Post is already liked"})
	post.user_likes.append(user)
	post.likes_amount += 1
	db.session.commit()
	
	return jsonify({'message': "Post liked"})

@api.route('/post/unlike', methods=['POST'])
@auth_required
def unlike_post(user):
	""" Unlike post """
	data = request.get_json()
	post_id = data.get('post_id')
	if not post_id:
		return jsonify({'error': "post_id is missing"})
	post = Post.query.filter_by(id=int(post_id)).first()
	if not post:
		return jsonify({'error': "post_id is incorrect"})
	if user not in post.user_likes:
		return jsonify({'error': "Post is not liked"})
	post.user_likes.remove(user)
	post.likes_amount -= 1
	db.session.commit()
	
	return jsonify({'message': "Post unliked"})