from flask import make_response, render_template, flash, request, redirect, url_for
from flask_restful import Resource
from flask_login import login_required, current_user

from models.students import Students
from models.teachers import Teachers


class Profile(Resource):
    @login_required
    def get(self, username, job):
        if current_user.job.lower() == "teacher" or username == current_user.username and job.lower() == 'student':
            person = Students.find_by_username(username, job) or Teachers.find_by_username(username, job)
            if person:
                data = {" ".join([person[x] for x in range(0, 2)]): [person[x] for x in range(2, len(person))]}
                return make_response(render_template("profile.html", data=data))
            # a single page of an person which includes all information
        else:
            return None


class Connections(Resource):
    def get(self, username, job):
        if current_user.username == username:
            try:
                if job.lower() == 'teacher':
                    student_usernames = Teachers.query.filter_by(username=current_user.username).first().student_usernames
                    students = Students.get_students_by_username(student_usernames)
                    if bool(students):
                        return make_response(render_template("connections.html", data=students))
                    else:
                        flash("You have not added anyone yet.")
                        return make_response(render_template("message.html"))
                elif job.lower() == 'student':
                    teacher_usernames = Students.query.filter_by(username=current_user.username).first().teacher_usernames
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
                return redirect(url_for("connections", username=current_user.username, job=current_user.job.lower()))
            elif job.lower() == 'student':
                remove_teacher = dict(request.form.items()).get("username")
                student = Students.query.filter_by(username=current_user.username).first()
                teachers = [*student.teacher_usernames]
                teachers.remove(remove_teacher)
                student.teacher_usernames = teachers
                student.save_to_db()
                return redirect(url_for("connections", username=current_user.username, job=current_user.job.lower()))

            else:
                flash("Please try again.")
                return make_response(render_template("message.html"))

        else:
            flash("Your username is not correct. Please try again.")
            return make_response(render_template("message.html"))


class AddConnection(Resource):
    def get(self, username, job):
        if current_user.username == username:
            try:
                if job.lower() == 'teacher':
                    student_usernames = Teachers.query.filter_by(username=current_user.username).first().student_usernames
                    students = Students.get_all_students()
                    return make_response(render_template("add_connection.html", data=students,
                                                         connections=student_usernames))
                elif job.lower() == 'student':
                    teacher_usernames = Students.query.filter_by(username=current_user.username).first().teacher_usernames
                    teachers = Teachers.get_all_teachers()
                    return make_response(render_template("add_connection.html", data=teachers,
                                                         connections=teacher_usernames))
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
                teacher = Teachers.query.filter_by(username=current_user.username).first()
                try:
                    students = [*teacher.student_usernames]
                except:
                    students = []

                students.append(new_student)
                teacher.student_usernames = students
                teacher.save_to_db()
                return redirect(url_for('addconnection', username=current_user.username, job=current_user.job.lower()))

            elif job.lower() == 'student':
                new_teacher = dict(request.form.items()).get("username")
                student = Students.query.filter_by(username=current_user.username).first()
                try:
                    teachers = [*student.teacher_usernames]
                except:
                    teachers = []

                teachers.append(new_teacher)
                student.teacher_usernames = teachers
                student.save_to_db()
                return redirect(url_for('addconnection', username=current_user.username, job=current_user.job.lower()))

            else:
                flash("Please try again.")
                return make_response(render_template("message.html"))

        else:
            flash("Your username is not correct. Please try again.")
            return make_response(render_template("message.html"))



