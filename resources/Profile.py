from flask import make_response, render_template
from flask_restful import Resource
from flask_login import login_required, current_user

from models.students import Students
from models.teachers import Teachers


class Profile(Resource):
    @login_required
    def get(self, username, job):
        print('get profile')
        if current_user.job.lower() == "teacher" or username == current_user.username and job.lower() == 'student':
            person = Students.find_by_username(username, job) or Teachers.find_by_username(username, job)
            if person:
                data = {" ".join([person[x] for x in range(0, 2)]): [person[x] for x in range(2, len(person))]}
                # student_usernames, teacher_username = Students.find_all_username(current_user.username)
                print(data)
                return make_response(render_template("profile.html", data=data))
            # a single page of an person which includes all information
        else:
            return None
