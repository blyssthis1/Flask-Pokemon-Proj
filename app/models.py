from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin,db.Model):
    id= db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable = True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password_hash = db.Column(db.String(120), nullable=True)
    posts = db.relationship('Post', backref = 'author', lazy = 'dynamic')
    pokemon = db.relationship('Pokemon', backref = 'owner', lazy = 'dynamic')

    def __repr__(self):
        return f'<User: {self.username}>'
    
    def __str__(self):
        return f'User: {self.email}|{self.username}'
    
    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


    def commit(self):
        db.session.add(self)
        db.session.commit()

class Post(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    heading = db.Column(db.String(40))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def commit(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'<Post: {self.body}>'
    


class Pokemon(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    pokemon_name=db.Column(db.String(240), nullable = False, unique=True)
    ability= db.Column(db.String(240))
    type=db.Column(db.String(240))
    sprite= db.Column(db.String(240))
    timestamp=db.Column(db.DateTime, default=datetime.utcnow)
    apiid = db.Column(db.Integer)
    user_id= db.Column(db.Integer, db.ForeignKey('user.id'), nullable =False)

    def __init__(self, pokemon_name, ability, type, sprite, apiid, user_id):
        self.pokemon_name = pokemon_name
        self.ability = ability
        self.type = type
        self.sprite = sprite
        self.apiid = apiid
        self.user_id = user_id

    def commit(self):
        db.session.add(self)
        db.session.commit()

    def delete_pokemon(self):
        db.session.delete(self)
        db.session.commit()