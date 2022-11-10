from flask import make_response, render_template
from flask_restful import Resource
from flask_login import login_required, current_user

from models.students import Students


class Profile(Resource):
    @login_required
    def get(self, username, job):
        student = Students.find_by_username(username, job)
        if student:
            data = {" ".join([student[x] for x in range(0, 2)]): [student[x] for x in range(2, len(student))]}
            student_usernames, teacher_username = Students.find_all_username(current_user.username)
            print(data)
            return make_response(render_template("profile.html", data=data, student_usernames=student_usernames,
                                                 teacher_username=teacher_username))
            # a single page of an student which includes all information
        else:
            return None
