

from database import db


class QNA(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    questions = db.Column(db.PickleType)
    answers = db.Column(db.PickleType)
    student_username = db.Column(db.String)
    status = db.Column(db.String)
    # teacher_username = db.Column(db.String)

    def __int__(self, questions, answers, student_username):
        self.questions = questions
        self.answers = answers
        self.student_username = student_username

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


