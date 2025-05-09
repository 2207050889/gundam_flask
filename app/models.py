from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login_manager

class Gundam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    series = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer)
    pilot = db.Column(db.String(100))
    height = db.Column(db.Float)
    weight = db.Column(db.Float)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(200))
    model_url = db.Column(db.String(200))
    
    comments = db.relationship('Comment', backref='gundam', lazy='dynamic')
    
    def __repr__(self):
        return f'<Gundam {self.name}>'


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    register_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    comments = db.relationship('Comment', backref='author', lazy='dynamic')
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    gundam_id = db.Column(db.Integer, db.ForeignKey('gundam.id'), nullable=False)
    
    def __repr__(self):
        return f'<Comment {self.id}>'


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id)) 