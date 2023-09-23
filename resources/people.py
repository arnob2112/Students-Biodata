from flask import make_response, render_template, flash, request, redirect, url_for
from flask_restful import Resource
from flask_login import login_required, current_user
import os

from models.users import Users
from models.students import Students
from models.teachers import Teachers
from models.requests import Requests


class Profile(Resource):
    @login_required
    def get(self, username, job):
        if current_user.job.lower() == "teacher" or username == current_user.username and job.lower() == 'student':
            person = Students.find_by_username(username, job) or Teachers.find_by_username(username, job)
            if person:
                data = {" ".join([person[x] for x in range(0, 2)]): [person[x] for x in range(2, len(person))]}
                return make_response(render_template("profile.html", data=data))
            # a single page of an person which includes all information
        elif current_user.job.lower() == "admin":
            person = Teachers.find_by_username(username, job)
            if person:
                data = {" ".join([person[x] for x in range(0, 2)]): [person[x] for x in range(2, len(person))]}
                return make_response(render_template("profile.html", data=data))
        else:
            flash("Please try again.")
            return make_response(render_template("message.html"))


class Connections(Resource):
    @login_required
    def get(self, username, job):
        if current_user.username == username:
            try:
                if job.lower() == 'teacher':
                    student_usernames = (Teachers.query.filter_by(username=current_user.username)
                                         .first().student_usernames)
                    print(student_usernames)
                    students = Students.get_students_by_username(student_usernames)
                    if bool(students):
                        return make_response(render_template("connections.html", data=students))
                    else:
                        flash("You have not added anyone yet.")
                        return make_response(render_template("message.html"))
                elif job.lower() == 'student':
                    teacher_usernames = Students.query.filter_by(
                        username=current_user.username).first().teacher_usernames
                    teachers = Teachers.get_teachers_by_username(teacher_usernames)
                    if bool(teachers):
                        return make_response(render_template("connections.html", data=teachers))
                    else:
                        flash("You have not added anyone yet.")
                        return make_response(render_template("message.html"))
                else:
                    flash("please try again.")
                    return make_response(render_template("message.html"))
            except Exception as e:
                print(e)
                flash("please try again.")
                return make_response(render_template("message.html"))
        else:
            flash("Your username is not correct. Please try again.")
            return make_response(render_template("message.html"))

    def post(self, username, job):
        print("connection post", dict(request.form.items()))
        if current_user.username == username:
            if job.lower() == 'teacher':
                remove_student = dict(request.form.items()).get("username")
                teacher = Teachers.query.filter_by(username=current_user.username).first()
                students = [*teacher.student_usernames]
                students.remove(remove_student)
                teacher.student_usernames = students
                teacher.save_to_db()

                student = Students.query.filter_by(username=remove_student).first()
                teachers = [*student.teacher_usernames]
                teachers.remove(current_user.username)
                student.teacher_usernames = teachers
                student.save_to_db()

                return redirect(url_for("connections", username=current_user.username, job=current_user.job.lower()))
            elif job.lower() == 'student':
                remove_teacher = dict(request.form.items()).get("username")
                student = Students.query.filter_by(username=current_user.username).first()
                teachers = [*student.teacher_usernames]
                teachers.remove(remove_teacher)
                student.teacher_usernames = teachers
                student.save_to_db()

                teacher = Teachers.query.filter_by(username=remove_teacher).first()
                students = [*teacher.student_usernames]
                students.remove(current_user.username)
                teacher.student_usernames = students
                teacher.save_to_db()

                return redirect(url_for("connections", username=current_user.username, job=current_user.job.lower()))

            else:
                flash("Please try again.")
                return make_response(render_template("message.html"))

        else:
            flash("Your username is not correct. Please try again.")
            return make_response(render_template("message.html"))


class AddConnection(Resource):
    @login_required
    def get(self, username, job):
        if current_user.username == username:
            try:
                if job.lower() == 'teacher':
                    student_usernames = (Teachers.query.filter_by(username=current_user.username)
                                         .first().student_usernames)
                    students = Students.get_all_students()
                    requested = (Requests.query.with_entities(Requests.student_username)
                                 .filter_by(teacher_username=current_user.username).all())
                    requested = [req[0] for req in requested]
                    print(requested)
                    return make_response(render_template("add_connection.html", data=students,
                                                         connections=student_usernames, requested=requested))
                elif job.lower() == 'student':
                    teacher_usernames = (Students.query.filter_by(username=current_user.username)
                                         .first().teacher_usernames)
                    teachers = Teachers.get_all_teachers()
                    requested = (Requests.query.with_entities(Requests.teacher_username)
                                 .filter_by(student_username=current_user.username).all())
                    requested = [req[0] for req in requested]
                    return make_response(render_template("add_connection.html", data=teachers,
                                                         connections=teacher_usernames, requested=requested))
                else:
                    flash("Please try again.")
                    return make_response(render_template("message.html"))
            except Exception as e:
                print(e)
                flash("please try again.")
                return make_response(render_template("message.html"))
        else:
            flash("Your username is not correct. Please try again.")
            return make_response(render_template("message.html"))

    def post(self, username, job):
        print("add connection post", dict(request.form.items()))
        if current_user.username == username:
            if job.lower() == 'teacher':
                new_student = dict(request.form.items()).get("username")
                new_pending = Requests(teacher_username=current_user.username, student_username=new_student,
                                       receiver_username=new_student)
                new_pending.save_to_db()

                return redirect(url_for('addconnection', username=current_user.username, job=current_user.job.lower()))

            elif job.lower() == 'student':
                new_teacher = dict(request.form.items()).get("username")
                new_pending = Requests(teacher_username=new_teacher, student_username=current_user.username,
                                       receiver_username=new_teacher)
                new_pending.save_to_db()

                return redirect(url_for('addconnection', username=current_user.username, job=current_user.job.lower()))

            else:
                flash("Please try again.")
                return make_response(render_template("message.html"))

        else:
            flash("Your username is not correct. Please try again.")
            return make_response(render_template("message.html"))


class All(Resource):
    @login_required
    def get(self, username, job):
        if current_user.username == username:
            if current_user.job.lower() == "admin":
                if job.lower() == "teacher":
                    teachers = Teachers.get_all_teachers()
                    return make_response(render_template("all.html", data=teachers))
                elif job.lower() == "student":
                    students = Students.get_all_students()
                    return make_response(render_template("all.html", data=students))
                else:
                    flash("Please try again.")
                    return make_response(render_template("message.html"))
            else:
                flash("You are not eligible for this")
                return make_response(render_template("message.html"))
        else:
            flash("Please check your username")
            return make_response(render_template("message.html"))

    def post(self, username, job):
        if current_user.username == username:
            if current_user.job.lower() == "admin":
                data = dict(request.form.items())
                if data.get("update") == "Update":
                    person = (Students.find_by_username(data['username'], data['job']) or
                              Teachers.find_by_username(data['username'], data['job']))
                    return make_response(render_template("update_form.html", data=person))
                elif data.get("delete") == "Delete":
                    if current_user.job.lower() == 'admin':
                        if data.get('job').lower() == 'teacher':
                            delete_teacher = Teachers.query.filter_by(username=data['username']).first()
                            flash("{} {} has deleted.".format(delete_teacher.firstname, delete_teacher.lastname))
                            delete_teacher.delete_from_db()
                        elif data.get('job').lower() == 'student':
                            delete_student = Students.query.filter_by(username=data['username']).first()
                            flash("{} {} has deleted.".format(delete_student.firstname, delete_student.lastname))
                            delete_student.delete_from_db()

                        # os.remove(Students.create_picture_path(data['username']))
                        # # removing from user table
                        # delete_user = Users.query.filter_by(username=data['username']).first()
                        # delete_user.delete_from_db()
                        return make_response(render_template("message.html"))
                    else:
                        flash("Please try again")
                        return make_response(render_template("message.html"))

                else:
                    flash("Please try again")
                    return make_response(render_template("message.html"))
            else:
                flash("You are not eligible for this")
                return make_response(render_template("message.html"))
        else:
            flash("Please check your username")
            return make_response(render_template("message.html"))
