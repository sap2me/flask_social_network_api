from flask import Blueprint, request, jsonify

from app import db
from app.models import User, Post
from app.tools import auth_required, json_response

from copy import deepcopy
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
		return json_response('Data required', 400)
	creation_time = datetime.datetime.utcnow()
	new_post = Post(text=text, creation_time=creation_time, likes_amount=0, author=user)

	db.session.add(new_post)
	db.session.commit()

	return json_response("Post created")

@api.route('/post/like', methods=['POST'])
@auth_required
def like_post(user):
	""" Like post """
	data = request.get_json()
	post_id = data.get('post_id')
	if not post_id:
		return json_response("post_id is missing", 400)
	post = Post.query.filter_by(id=int(post_id)).first()
	if not post:
		return json_response("post_id is incorrect", 400)
	if user in post.user_likes:
		return json_response("Post is already liked", 400)
	post.user_likes.append(user)
	post.likes_amount += 1
	db.session.commit()
	
	return json_response("Post liked")

@api.route('/post/unlike', methods=['POST'])
@auth_required
def unlike_post(user):
	""" Unlike post """
	data = request.get_json()
	post_id = data.get('post_id')
	if not post_id:
		return json_response("post_id is missing", 400)
	post = Post.query.filter_by(id=int(post_id)).first()
	if not post:
		return json_response("post_id is incorrect", 400)
	if user not in post.user_likes:
		return json_response("Post is not liked", 400)
	post.user_likes.remove(user)
	post.likes_amount -= 1
	db.session.commit()
	
	return json_response("Post unliked")

@api.route('/posts', methods=['GET'])
def get_post():
	""" Get all posts """
	date_from = request.args.get('date_from')
	date_to = request.args.get('date_to')
	posts = Post.query
	if date_from:
		date_from = datetime.datetime.fromisoformat(date_from)
		posts = posts.filter(Post.creation_time >= date_from)
	if date_to:
		date_to = datetime.datetime.fromisoformat(date_to)
		posts = posts.filter(Post.creation_time <= date_to)

	posts_list = []
	for post in posts:
		posts_list.append({
			"text": post.text,
			"author": post.author.name,
			"likes_amount": post.likes_amount,
			"users_likes": [user.name for user in post.user_likes],
			"creation_time": post.creation_time
		})
	return jsonify(posts_list)

@api.route('/analitics/', methods=['GET'])
def analitics():
	""" Analitics about single/all posts """
	date_from = request.args.get('date_from')
	date_to = request.args.get('date_to')
	sort_by = request.args.get('sort_by')
	sort_typies = ['year', 'month', 'day', 'hour', 'minute']
	if not sort_by in sort_typies:
		sort_by = 'day'
	posts = Post.query.order_by(Post.creation_time.desc())
	if date_from:
		date_from = datetime.datetime.fromisoformat(date_from)
		posts = posts.filter(Post.creation_time >= date_from)
	if date_to:
		date_to = datetime.datetime.fromisoformat(date_to)
		posts = posts.filter(Post.creation_time <= date_to)

	first_date = posts.first().creation_time
	last_day = getattr(first_date, sort_by)
	days_list = []
	day_list = []
	likes = 0
	for ind, post in enumerate(posts):
		current_day = getattr(post.creation_time, sort_by)
		if current_day != last_day or ind == posts.count() - 1:
			days_list.append({
				"posts": deepcopy(day_list),
				"likes": likes
			})
			day_list.clear()
			likes = 0
		likes += post.likes_amount
		day_list.append({
			"text": post.text,
			"author": post.author.name,
			"likes_amount": post.likes_amount,
			"users_likes": [user.name for user in post.user_likes],
			"creation_time": post.creation_time
		})
		last_day = current_day

	return jsonify(days_list)

@api.route('/users/<int:user_id>', methods=['GET'])
def user_activity(user_id):
	""" User last login/activity informaiton """
	user = User.query.filter_by(id=user_id).first()
	if not user:
		return json_response('There is no users with this id', 400)
	data = {
		"success": True,
		"last_login": user.last_login,
		"last_activity": user.last_activity
	}
	return jsonify(data)