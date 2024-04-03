from itertools import zip_longest
from flask_login import current_user
from werkzeug.utils import secure_filename
import os

from database import db


class QNA(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    questions = db.Column(db.PickleType)
    answers = db.Column(db.PickleType)
    picture_path = db.Column(db.PickleType)
    audio_path = db.Column(db.PickleType)
    student_username = db.Column(db.String)
    status = db.Column(db.String)

    # teacher_username = db.Column(db.String)

    def __int__(self, questions, answers, picture_path, audio_path, student_username):
        self.questions = questions
        self.answers = answers
        self.picture_path = picture_path
        self.audio_path = audio_path
        self.student_username = student_username

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def all_questions():
        if current_user.job.lower() == "teacher":
            all_questions = (QNA.query.with_entities(QNA.questions, QNA.answers, QNA.id, QNA.student_username)
                             .filter_by(status="Pending").all())
        else:
            all_questions = QNA.query.with_entities(QNA.questions, QNA.answers, QNA.id, QNA.student_username).all()
        sorted_all_questions = []
        for questions in all_questions:
            qna = dict(zip_longest(questions[0], questions[1], fillvalue="Pending"))
            sorted_all_questions.append([qna, questions[2], questions[3]])
        sorted_all_questions.reverse()
        return sorted_all_questions

    @staticmethod
    def my_questions():
        all_questions = (QNA.query.with_entities(QNA.questions, QNA.answers, QNA.id, QNA.student_username)
                         .filter_by(student_username=current_user.username).all())
        sorted_all_questions = []
        for questions in all_questions:
            qna = dict(zip_longest(questions[0], questions[1], fillvalue="Pending"))
            sorted_all_questions.append([qna, questions[2], questions[3]])
        sorted_all_questions.reverse()
        return sorted_all_questions

    @staticmethod
    def create_audio_path():
        next_id = str(QNA.query.order_by(QNA.id.desc()).first().id + 1)
        upload_folder = os.path.join('static', 'audios')
        # audio_filename = secure_filename("{}_{}.mp3".format(current_user.username, next_id))
        audio_filename = secure_filename(f"{current_user.username}_{next_id}.mp3")
        audio_path = os.path.join(upload_folder, audio_filename)
        return audio_path

    @staticmethod
    def create_picture_path():
        next_id = str(QNA.query.order_by(QNA.id.desc()).first().id + 1)
        upload_folder = os.path.join('static', 'question_pictures')
        picture_filename = secure_filename(f"{current_user.username}_{next_id}.jpg")
        picture_path = os.path.join(upload_folder, picture_filename)
        return picture_path

