from flask_login import current_user

from database import db


class Notifications(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer)
    question = db.Column(db.String)
    sender = db.Column(db.String)
    receiver = db.Column(db.String)
    status = db.Column(db.String)

    def __init__(self, question_id, question, sender, receiver, status):
        self.question_id = question_id
        self.question = question
        self.sender = sender
        self.receiver = receiver
        self.status = status

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def pending():
        if current_user.is_authenticated:
            notifications = Notifications.query.filter_by(receiver=current_user.username, status="pending").count()
            return notifications
        else:
            return None
