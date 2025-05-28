from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login

class Gundam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    series = db.Column(db.String(50), nullable=False)
    year = db.Column(db.String(20))
    height = db.Column(db.Float)
    weight = db.Column(db.Float)
    pilot = db.Column(db.String(100))
    brief_intro = db.Column(db.Text)  # 简洁介绍，用于缩略图和详情页顶部
    description = db.Column(db.Text)  # 详细描述，用于详情页详细介绍部分
    image_url = db.Column(db.String(200))
    model_url = db.Column(db.String(200))
    
    # New fields for radar chart data
    size = db.Column(db.String(255), nullable=True)  # e.g., "头顶高：18.0米；全高：18.5米"
    base_weight = db.Column(db.String(255), nullable=True)  # e.g., "43.4吨"
    full_weight = db.Column(db.String(255), nullable=True)  # e.g., "60.0吨"
    engine_power = db.Column(db.String(255), nullable=True)  # e.g., "1380KW"
    thrust = db.Column(db.String(255), nullable=True)  # e.g., "55500KG"
    acceleration = db.Column(db.String(255), nullable=True)  # e.g., "0.93G"
    
    comments = db.relationship('Comment', backref='gundam', lazy='dynamic')
    
    def __repr__(self):
        return f'<Gundam {self.name}>'


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
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
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    gundam_id = db.Column(db.Integer, db.ForeignKey('gundam.id'), nullable=False)
    
    def __repr__(self):
        return f'<Comment {self.id}>'


@login.user_loader
def load_user(id):
    return User.query.get(int(id)) 