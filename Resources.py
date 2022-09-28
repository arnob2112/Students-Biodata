from flask import render_template, make_response
from flask_restful import Resource, reqparse
import sqlite3


class Home(Resource):
    TABLE_NAME = 'people'

    def get(self):
        connection = sqlite3.connect("All Information.db")
        cursor = connection.cursor()
        result = list(cursor.execute("SELECT FirstName, LastName, Contact_Number FROM {}".format(self.TABLE_NAME)).
                      fetchall())
        data = {}
        for item in result:
            data[" ".join([item[x] for x in range(2)])] = item[2]
        return make_response(render_template("home.html", data=data))


class ReceiveInfo(Resource):
    TABLE_NAME = 'people'

    parser = reqparse.RequestParser()
    parser.add_argument('firstname',
                        type=str,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('lastname',
                        type=str,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('gender',
                        type=str)
    parser.add_argument('religion',
                        type=str)
    parser.add_argument('job',
                        type=str)
    parser.add_argument('college',
                        type=str)
    parser.add_argument('age',
                        type=str)
    parser.add_argument('number',
                        type=str)
    parser.add_argument('fb_url')

    def post(self):
        data = ReceiveInfo.parser.parse_args()
        connection = sqlite3.connect("All Information.db")
        cursor = connection.cursor()
        query = "INSERT INTO {} VALUES(NULL, ? , ?, ?, ?, ?, ?, ?, ?, ?)".format(self.TABLE_NAME)
        cursor.execute(query, (data['firstname'], data['lastname'], data['college'], data['age'], data['gender'],
                               data['religion'], data['number'], data['fb_url'], data['job']))
        connection.commit()
        connection.close()
        return make_response(render_template("updated.html", name="{} {}".format(data['firstname'], data['lastname'],
                                                                                 data['gender'], data['religion'],
                                                                                 data['job'])))

    def get(self):
        return make_response(render_template("form.html"))


class GetInfo(Resource):
    TABLE_NAME = "user"

    parser = reqparse.RequestParser()
    parser.add_argument("username",
                        type=str,
                        required=True,
                        help="Username can't be blank.")
    parser.add_argument("password",
                        type=str,
                        required=True,
                        help="Password can't left blank.")

    def get(self):
        return make_response(render_template("login.html"))

    def post(self):
        data = GetInfo.parser.parse_args()
        connection = sqlite3.connect("All Information.db")
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM user WHERE username=?", (data['username'],)).fetchone()
        if result:
            user = result
        else:
            user = None
        if user[1] == data['password']:
            query = "SELECT * FROM people"
            data = list(cursor.execute(query))
            info = {}
            for item in data:
                info[" ".join([item[x] for x in range(1, 3)])] = [item[a] for a in range(3, len(item))]
        else:
            return {"message": "You have entered wrong password."}

        connection.commit()
        connection.close()
        return make_response(render_template("showinfo.html", data=info))
