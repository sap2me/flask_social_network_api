from app import db


class User(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True)
	password = db.Column(db.String(128))
	posts = db.relationship('Post', backref='author')

	def __repr__(self):
		return f"<User {self.name}>"

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	text = db.Column(db.String(500))
	creation_time = db.Column(db.DateTime)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return f"<Post {self.id}>"