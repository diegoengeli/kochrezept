# app/models.py
# code used from microblog [Miguel Grinberg]
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db, login

# code by marcel based on microblog [Miguel Grinberg]
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    street = db.Column(db.String(128))
    city = db.Column(db.String(64))
    postal_code = db.Column(db.String(20))
    country = db.Column(db.String(64))
    recipes = db.relationship('Recipe', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.email)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# code by marcel based on microblog [Miguel Grinberg]
class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    image_filename = db.Column(db.String(140))
    ingredients = db.Column(db.Text)
    instructions = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Recipe {self.title}>'
    
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
