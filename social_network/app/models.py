from app import db

likes = db.Table('likes',
		db.Column('id', db.Integer, primary_key=True),
		db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
		db.Column('post_id', db.Integer, db.ForeignKey('posts.id'))
	)

class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True)
	password = db.Column(db.String(128))
	last_login = db.Column(db.DateTime, nullable=True)
	last_activity = db.Column(db.DateTime)
	posts = db.relationship('Post', backref='author')
	post_likes = db.relationship('Post', secondary=likes, backref='user')

	def __repr__(self):
		return f"<User {self.name}>"

class Post(db.Model):
	__tablename__ = 'posts'
	id = db.Column(db.Integer, primary_key=True)
	text = db.Column(db.String(500))
	creation_time = db.Column(db.DateTime)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	likes_amount = db.Column(db.Integer, nullable=True)
	user_likes = db.relationship('User', secondary=likes, backref='post')

	def __repr__(self):
		return f"<Post {self.id}>"