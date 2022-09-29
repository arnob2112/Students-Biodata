from flask import render_template, make_response
from flask_restful import Resource, reqparse
import sqlite3


class Student:
    def __init__(self, firstname):
        self.firstname = firstname

    @classmethod
    def find_by_firstname(cls, name):
        connection = sqlite3.connect("All Information.db")
        cursor = connection.cursor()

        query = "SELECT * FROM people WHERE Username=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        if row:
            return list(row)
        else:
            student = None

        connection.close()
        return student

    @staticmethod
    def find_username():
        connection = sqlite3.connect("All Information.db")
        cursor = connection.cursor()
        users = list(cursor.execute("SELECT FirstName, LastName, Username FROM people ").fetchall())
        usernames = {}
        for user in users:
            usernames[" ".join([user[x] for x in range(2)])] = user[2]
        return usernames


class Profile(Resource):
    def get(self, name):
        student = Student.find_by_firstname(name)
        if student:
            data = {" ".join([student[x] for x in range(1, 3)]): [student[x] for x in range(3, len(student) - 1)]}
            usernames = Student.find_username()
            return make_response(render_template("profile.html", data=data, user=usernames))
        else:
            return None
