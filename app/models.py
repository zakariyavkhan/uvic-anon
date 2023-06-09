from . import db, login_manager
from sqlalchemy.sql import func
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    verified = db.Column(db.Boolean, default=False)
    posts = db.relationship('Post', backref='user', lazy=True)
    comments = db.relationship('Comment', backref='user', lazy=True) 
    votes = db.relationship('Vote', backref='user', lazy=True)

    def check_password(self, attempted_password):
        return self.password == attempted_password

    def __repr__(self):
        return f'User {self.username}'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime(timezone=True), unique=False, default=func.now())
    expired = db.Column(db.Boolean, nullable=False, default=False)
    content = db.Column(db.String, nullable=False)
    comments = db.relationship('Comment', backref='post', lazy=True)
    votes = db.relationship('Vote', backref='post', lazy=True)
    
    def __repr__(self):
        return f'Post ID {self.id}'

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    def __repr__(self):
        return f'Comment ID {self.id}'
    
class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vote_type = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    
    def __repr__(self):
        if self.vote_type:
            return f'(upvote, user_id:{self.user_id}, post_id:{self.post_id})'
        else:
            return f'(downvote, user_id:{self.user_id}, post_id:{self.post_id})'