import sqlite3
import os
from werkzeug.utils import secure_filename
from flask_login import current_user
import random

from database import db


class Students(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    Firstname = db.Column(db.String(1000))
    Lastname = db.Column(db.String(1000))
    College = db.Column(db.String(1000))
    Age = db.Column(db.Integer)
    Gender = db.Column(db.String(1000))
    Religion = db.Column(db.String(1000))
    Contact_Number = db.Column(db.String(20))
    FB_URL = db.Column(db.String(1000))
    Job = db.Column(db.String(100))
    Image_Path = db.Column(db.String(1000))
    Username = db.Column(db.String(1000), unique=True)
    Teacher_Username = db.Column(db.String(1000))

    def __init__(self, firstname, lastname, college, age, gender, religion,
                 contact_number, fb_url, job, image_path, username, teacher_username):
        self.Firstname = firstname
        self.Lastname = lastname
        self.College = college
        self.Age = age
        self.Gender = gender or 23
        self.Religion = religion or None
        self.Contact_Number = contact_number
        self.FB_URL = fb_url
        self.Job = job
        self.Image_Path = image_path
        self.Username = username
        self.Teacher_Username = teacher_username

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def find_by_username(username, job):
        # connection = sqlite3.connect("All Information.db")
        # cursor = connection.cursor()
        # query = "SELECT * FROM people WHERE Username=?"
        # result = cursor.execute(query, (name,)).fetchone()
        # connection.commit()
        # connection.close()

        result = Students.query.with_entities(Students.Firstname, Students.Lastname, Students.College, Students.Age,
                                              Students.Gender, Students.Religion, Students.Contact_Number,
                                              Students.FB_URL, Students.Job, Students.Image_Path,
                                              Students.Username)\
            .filter_by(Username=username, Teacher_Username=current_user.username, Job=job.capitalize()).first()
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
        firstnames = Students.query.with_entities(Students.Firstname).all()
        return firstnames  # returning all firstnames in list of tuples

    @staticmethod
    def find_all_username(teacher):
        # connection = sqlite3.connect("All Information.db")
        # cursor = connection.cursor()
        # users = list(cursor.execute("SELECT FirstName, LastName, Username FROM people ").fetchall())
        # connection.commit()
        # connection.close()

        students = Students.query.with_entities(Students.Firstname, Students.Lastname, Students.Username)\
            .filter_by(Teacher_Username=teacher, Job="Student").all()
        student_usernames = []
        for student in students:
            student_usernames.append(tuple([" ".join(student[x] for x in range(2)), student[2]]))
        try:
            teacher_username = Students.query.with_entities(Students.Username)\
                .filter_by(Teacher_Username=current_user.username, Job="Teacher").first()[0]
        except:
            teacher_username = None
        return student_usernames, teacher_username
        # returning all usernames in list of tuples -> (FirstName + LastName, Username)

    @staticmethod
    def find_username(firstname):
        # connection = sqlite3.connect("All Information.db")
        # cursor = connection.cursor()
        # username = cursor.execute("SELECT Username FROM people WHERE FirstName=?", (firstname, )).fetchone()
        # connection.commit()
        # connection.close()
        username = Students.query.with_entities(Students.Username).filter_by(Firstname=firstname).first()
        print(username)
        return username  # returning username in tuple -> (username, )

    @staticmethod
    def generate_username(firstname, teacher_username):
        usernames = [user[0] for user in Students.query.with_entities(Students.Username).all()]
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
        all_data = Students.query.with_entities(Students.Firstname, Students.Lastname, Students.College, Students.Age,
                                                Students.Gender, Students.Religion, Students.Contact_Number,
                                                Students.FB_URL, Students.Job, Students.Image_Path,
                                                Students.Username)\
            .filter_by(Teacher_Username=teacher_username, Job="Student").all()
        return all_data

    @staticmethod
    def find_name_by_username(username):
        # connection = sqlite3.connect("All Information.db")
        # cursor = connection.cursor()
        # query = "SELECT FirstName, Lastname FROM people WHERE Username=?"
        result = Students.query.with_entities(Students.Firstname, Students.Lastname)\
            .filter_by(Username=username).first()
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
