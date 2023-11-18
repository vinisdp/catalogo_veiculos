# models/user.py
import hashlib
from db import db
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from typing import List

class UserModel(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __init__(self, username, name, password, email):
        self.username = username
        self.name = name
        self.password = password
        self.email = email

    def json(self):
        return {'username': self.username, 'name': self.name, 'email': self.email}

    
    
    @classmethod
    def find_all(cls) -> List["UserModel"]:
        return cls.query.all()
    
    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @staticmethod
    def authenticate(username, password):
        user = UserModel.find_by_username(username)
        if user and user.check_password(password):
            return user
        return None
    
    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()