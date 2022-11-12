from flask_login import UserMixin

from database import db


class Users(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = password
