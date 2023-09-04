import sqlite3
import os
from werkzeug.utils import secure_filename
from flask_login import current_user
import random

from database import db


class Students(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(1000))
    lastname = db.Column(db.String(1000))
    college = db.Column(db.String(1000))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(1000))
    religion = db.Column(db.String(1000))
    contact_number = db.Column(db.String(20))
    fb_url = db.Column(db.String(1000))
    job = db.Column(db.String(100))
    image_path = db.Column(db.String(1000))
    username = db.Column(db.String(1000), unique=True)
    teacher_username = db.Column(db.String(1000))

    def __init__(self, firstname, lastname, college, age, gender, religion,
                 contact_number, fb_url, job, image_path, username, teacher_username):
        self.firstname = firstname
        self.lastname = lastname
        self.college = college
        self.age = age
        self.gender = gender or 23
        self.religion = religion or None
        self.contact_number = contact_number
        self.fb_url = fb_url
        self.job = job
        self.image_path = image_path
        self.username = username
        self.teacher_username = teacher_username

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def find_by_username(username, job):
        result = Students.query.with_entities(Students.firstname, Students.lastname, Students.college, Students.age,
                                              Students.gender, Students.religion, Students.contact_number,
                                              Students.fb_url, Students.job, Students.image_path,
                                              Students.username) \
            .filter_by(username=username, job=job.capitalize()).first()  # teacher_username=current_user.username,
        if result:
            return list(result)  # returning all information of a student in list
        else:
            return None

    @staticmethod
    def find_all_firstname():
        # connection = sqlite3.connect("All Information.db")
        # cursor = connection.cursor()
        # firstnames = list(cursor.execute("SELECT FirstName FROM people").fetchall())
        # connection.commit()
        # connection.close()
        firstnames = Students.query.with_entities(Students.firstname).all()
        return firstnames  # returning all firstnames in list of tuples

    @staticmethod
    def find_all_username(teacher): #need to check usage
        # connection = sqlite3.connect("All Information.db")
        # cursor = connection.cursor()
        # users = list(cursor.execute("SELECT FirstName, LastName, username FROM people ").fetchall())
        # connection.commit()
        # connection.close()

        students = Students.query.with_entities(Students.firstname, Students.lastname, Students.username) \
            .filter_by(teacher_username=teacher, job="Student").all()
        student_usernames = []
        for student in students:
            student_usernames.append(tuple([" ".join(student[x] for x in range(2)), student[2]]))
        try:
            teacher_username = Students.query.with_entities(Students.username) \
                .filter_by(teacher_username=current_user.username, job="Teacher").first()[0]
        except:
            teacher_username = None
        return student_usernames, teacher_username
        # returning all usernames in list of tuples -> (FirstName + LastName, username)

    @staticmethod
    def find_username(firstname):
        # connection = sqlite3.connect("All Information.db")
        # cursor = connection.cursor()
        # username = cursor.execute("SELECT username FROM people WHERE FirstName=?", (firstname, )).fetchone()
        # connection.commit()
        # connection.close()
        username = Students.query.with_entities(Students.username).filter_by(firstname=firstname).first()
        print(username)
        return username  # returning username in tuple -> (username, )

    @staticmethod
    def generate_username(firstname, teacher_username):
        usernames = [user[0] for user in Students.query.with_entities(Students.username).all()]
        unique_username = firstname.lower()
        while True:
            if unique_username not in usernames:
                print("unique username", unique_username)
                return unique_username
            else:
                random_number = random.randint(0, 100)
                unique_username = unique_username + str(random_number)

    @staticmethod
    def find_picture(username):
        upload_folder = os.path.join('static', 'pictures')
        img_filename = secure_filename(username + ".jpg")
        image_path = os.path.join(upload_folder, img_filename)
        return image_path  # creating picture path using firstname -> static\pictures\firstname.jpg

    @staticmethod
    def get_all_students(teacher_username):
        # connection = sqlite3.connect("All Information.db")
        # cursor = connection.cursor()
        # query = "SELECT * FROM people"
        # all_data = list(cursor.execute(query))
        # connection.commit()
        # connection.close()
        all_data = Students.query.with_entities(Students.firstname, Students.lastname, Students.college, Students.age,
                                                Students.gender, Students.religion, Students.contact_number,
                                                Students.fb_url, Students.job, Students.image_path,
                                                Students.username) \
            .filter_by(teacher_username=teacher_username, job="Student").all()
        return all_data  # return all students' info of teacher's username

    @staticmethod
    def find_name_by_username(username):
        # connection = sqlite3.connect("All Information.db")
        # cursor = connection.cursor()
        # query = "SELECT FirstName, Lastname FROM people WHERE username=?"
        result = Students.query.with_entities(Students.firstname, Students.lastname) \
            .filter_by(username=username).first()
        name = " ".join(result)
        return name

    @staticmethod
    def divide_in_there(persons):
        teacher = persons[0]
        persons.pop(0)
        students = []
        extra = len(persons) % 3
        if extra:
            for a in range(0, len(persons) - extra, 3):
                groups = []
                for b in range(3):
                    groups.append(persons[0])
                    persons.pop(0)
                students.append(tuple(groups))
            extra_group = []
            while persons:
                extra_group.append(persons[0])
                persons.pop(0)
            students.append(tuple(extra_group))

        else:
            for a in range(0, len(persons), 3):
                groups = []
                for b in range(3):
                    groups.append(persons[0])
                    persons.pop(0)
                students.append(tuple(groups))
        return teacher, students

    @staticmethod
    def divide(persons):
        teacher = persons[0]
        persons.pop(0)
        students = tuple(persons)
        return teacher, students
