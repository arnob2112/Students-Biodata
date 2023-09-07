from flask_login import current_user

from models.students import Students
from database import db


class Teachers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String)
    lastname = db.Column(db.String)
    college = db.Column(db.String)
    age = db.Column(db.Integer)
    gender = db.Column(db.String)
    religion = db.Column(db.String)
    contact_number = db.Column(db.String)
    email = db.Column(db.String)
    fb_url = db.Column(db.String)
    job = db.Column(db.String)
    image_path = db.Column(db.String)
    username = db.Column(db.String, unique=True)
    student_usernames = db.Column(db.PickleType)

    def __int__(self, firstname, lastname, college, age, gender,
                religion, contact_number, email, fb_url, job, image_path, username, student_usernames):
        self.firstname = firstname
        self.lastname = lastname
        self.college = college
        self.age = age
        self.gender = gender
        self.religion = religion
        self.contact_number = contact_number
        self.email = email
        self.fb_url = fb_url
        self.job = job
        self.image_path = image_path
        self.username = username
        self.student_usernames = student_usernames

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def find_by_username(username, job):
        result = Teachers.query.with_entities(Teachers.firstname, Teachers.lastname, Teachers.college, Teachers.age,
                                              Teachers.gender, Teachers.religion, Teachers.contact_number,
                                              Teachers.fb_url, Teachers.job, Teachers.image_path,
                                              Teachers.username) \
            .filter_by(username=username, job=job.capitalize()).first()
        if result:
            return list(result)  # returning all information of a student in list
        else:
            return None

    @staticmethod
    def get_all_teachers():
        all_teachers = Teachers.query.with_entities(Teachers.firstname, Teachers.lastname, Teachers.college,
                                                    Teachers.age, Teachers.gender, Teachers.religion,
                                                    Teachers.contact_number, Teachers.fb_url, Teachers.job,
                                                    Teachers.image_path, Teachers.username)\
            .filter_by(job="Teacher").all()
        return all_teachers

    @staticmethod
    def get_teachers_by_username(teachers_usernames: list):
        all_teachers = []

        try:
            for username in teachers_usernames:
                teacher = Teachers.query.with_entities(Teachers.firstname, Teachers.lastname, Teachers.college,
                                                       Teachers.age, Teachers.gender, Teachers.religion,
                                                       Teachers.contact_number, Teachers.fb_url, Teachers.job,
                                                       Teachers.image_path, Teachers.username) \
                    .filter_by(username=username).first()
                all_teachers.append(teacher)
            return tuple(all_teachers)
        except Exception as e:
            print(e)
            return None

        # returning all teachers' information by using their username who are connected with current student in tuple
