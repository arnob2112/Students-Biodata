from flask_login import UserMixin

from database import db


class Users(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    job = db.Column(db.String(100))
    verified = db.Column(db.Integer)

    def __init__(self, email, username, password, job, verified):
        self.username = username
        self.password = password
        self.email = email
        self.job = job
        self.verified = verified

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


