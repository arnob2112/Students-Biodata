from flask_login import current_user

from models.teachers import Teachers
from models.students import Students
from database import db


class Requests(db.Model):  # this name should be connection requests
    id = db.Column(db.Integer, primary_key=True)
    teacher_username = db.Column(db.String)
    student_username = db.Column(db.String)
    receiver_username = db.Column(db.String)

    def __int__(self, teacher_username, student_username, receiver_username):
        self.teacher_username = teacher_username
        self.student_username = student_username
        self.receiver_username = receiver_username

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all_requests():
        print("get all request")
        if current_user.job.lower() == 'teacher':
            request_usernames = Requests.query.with_entities(Requests.student_username).\
                                 filter_by(teacher_username=current_user.username,
                                           receiver_username=current_user.username).all()
            request_usernames = [username[0] for username in request_usernames]
            if bool(request_usernames):
                all_requests = Students.get_students_by_username(request_usernames)
                return all_requests
            else:
                return None

        elif current_user.job.lower() == 'student':
            request_usernames = (Requests.query.with_entities(Requests.teacher_username).
                                 filter_by(student_username=current_user.username,
                                           receiver_username=current_user.username)).all()
            request_usernames = [username[0] for username in request_usernames]
            if bool(request_usernames):
                all_requests = Teachers.get_teachers_by_username(request_usernames)
                return all_requests
            else:
                return None
        else:
            return None
