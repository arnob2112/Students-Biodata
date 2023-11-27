from flask import make_response, render_template, flash, request, redirect, url_for
from flask_restful import Resource
from flask_login import login_required, current_user

from models.teachers import Teachers
from models.students import Students
from models.connectionrequests import ConnectionRequests
from models.notifications import Notifications


class ConnectionPending(Resource):  # this name should be connection requests
    TABLE_NAME = "pending"

    @login_required
    def get(self, username, job):
        if current_user.username == username:
            if job.lower() == 'teacher':
                all_requests = ConnectionRequests.get_all_requests()
                print("get method request", all_requests)
                if bool(all_requests):
                    return make_response(render_template("requests.html", data=all_requests,
                                                         notify=Notifications.pending()))
                else:
                    flash("You have no requests.")
                    return make_response(render_template("message.html"))
            if job.lower() == 'student':
                all_requests = ConnectionRequests.get_all_requests()
                if bool(all_requests):
                    return make_response(render_template("requests.html", data=all_requests,
                                                         notify=Notifications.pending()))
                else:
                    flash("You have no requests.")
                    return make_response(render_template("message.html"))
            else:
                flash("Please try again.")
                return make_response(render_template("message.html"))
        else:
            flash("Please check your username. try again.")
            return make_response(render_template("message.html"))

    @login_required
    def post(self, username, job):
        print("pending post")
        if current_user.username == username:
            if job.lower() == 'teacher':
                new_student = dict(request.form.items()).get("username")
                print("new", new_student, dict(request.form.items()))
                teacher = Teachers.query.filter_by(username=current_user.username).first()
                try:
                    students = [*teacher.student_usernames]
                except:
                    students = []
                students.append(new_student)
                teacher.student_usernames = students
                teacher.save_to_db()

                student = Students.query.filter_by(username=new_student).first()
                try:
                    teachers = [*student.teacher_usernames]
                except:
                    teachers = []

                teachers.append(current_user.username)
                student.teacher_usernames = teachers
                student.save_to_db()

                delete_request = ConnectionRequests.query.filter_by(teacher_username=current_user.username,
                                                                    student_username=new_student).first()
                delete_request.delete_from_db()

                return redirect(url_for('connectionpending', username=current_user.username, job=current_user.job.lower()))

            elif job.lower() == 'student':
                new_teacher = dict(request.form.items()).get("username")
                print("new", new_teacher, dict(request.form.items()))
                student = Students.query.filter_by(username=current_user.username).first()
                try:
                    teachers = [*student.teacher_usernames]
                except:
                    teachers = []

                teachers.append(new_teacher)
                student.teacher_usernames = teachers
                student.save_to_db()

                teacher = Teachers.query.filter_by(username=new_teacher).first()
                try:
                    students = [*teacher.student_usernames]
                except:
                    students = []
                students.append(current_user.username)
                teacher.student_usernames = students
                teacher.save_to_db()

                delete_request = ConnectionRequests.query.filter_by(teacher_username=new_teacher,
                                                                    student_username=current_user.username).first()
                delete_request.delete_from_db()

                return redirect(url_for('connectionpending', username=current_user.username, job=current_user.job.lower()))
            else:
                flash("Please try again.")
                return make_response(render_template("message.html"))

        else:
            flash("Your username is not correct. Please try again.")
            return make_response(render_template("message.html"))

