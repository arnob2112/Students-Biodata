from flask import render_template, make_response, request, session
from flask_restful import Resource
from flask_login import login_required, current_user
import requests
import os

from models.students import Students
from models.teachers import Teachers
from database import db


class Home(Resource):
    TABLE_NAME = 'people'

    def get(self):
        if current_user.is_authenticated:
            if Students.query.filter_by(username=current_user.username).first() is None and Teachers.query.filter_by(
                    username=current_user.username).first() is None:
                return make_response(render_template("form.html"))
        return make_response(render_template("home.html"))


class ReceiveInfo(Resource):
    TABLE_NAME = 'people'

    def get(self, job):
        return make_response(render_template("form.html", job=job.lower()))

    def post(self, job):
        data = dict(request.form.items())

        # initializing put method
        if data['work'] == 'Update':
            info = Students.find_by_username(data['username'], data['job'].capitalize())
            return make_response(render_template("update_form.html", data=info))

        elif data['work'] == 'init update':
            if request.files['Picture']:
                data['Picture'] = True
            else:
                data['Picture'] = False

            requests.put(request.url, params=data, files={'Picture': request.files['Picture']})

            students = Students.get_all_students(current_user.username)
            return make_response(
                render_template("showinfo.html", students=students,
                                message="{} {} has updated.".format(data['firstname'], data['Lastname'])))

        # initializing delete method
        elif data["work"] == 'Delete':
            name = Students.find_name_by_username(data['username'])
            requests.delete(request.url, params=data)

            all_students = Students.get_all_students(current_user.username)
            return make_response(render_template("showinfo.html", students=all_students,
                                                 message="{} has deleted.".format(name)))

        else:
            if current_user.is_authenticated:
                teacher_username = None  # need to be fixed
            else:
                teacher_username = data['teacher_username']

            # saving picture in pictures folder and path in database
            image_path = Students.create_picture_path(current_user.username)
            uploaded_img = request.files['picture']
            uploaded_img.save(image_path)

            if current_user.job.lower() == 'student':
                new_student = Students(firstname=data['firstname'], lastname=data['lastname'], college=data['college'],
                                       age=data['age'], gender=data.get('gender'), religion=data.get('religion'),
                                       contact_number=data['number'], fb_url=data['fb_url'], job=job.capitalize(),
                                       image_path=image_path, username=current_user.username,
                                       teacher_username=teacher_username)
                new_student.save_to_db()

            else:
                new_teacher = Teachers(firstname=data['firstname'], lastname=data['lastname'], college=data['college'],
                                       age=data['age'], gender=data.get('gender'), religion=data.get('religion'),
                                       contact_number=data['number'], fb_url=data['fb_url'], job=job.capitalize(),
                                       image_path=image_path, username=current_user.username, )
                new_teacher.save_to_db()

            return make_response(render_template("uploaded.html",
                                                 name="{} {}".format(data['firstname'], data['lastname'], )))

    def put(self):
        data = dict(request.args)

        image_path = Students.create_picture_path(data['username'])
        if data['Picture'] == "True":
            uploaded_img = request.files['Picture']
            uploaded_img.save(image_path)
            session['uploaded_img_file_path'] = image_path

        data.pop('work')
        data.pop('Picture')
        Students.query.filter_by(username=data['username']).update(data)
        db.session.commit()

        return None

    def delete(self):
        # need to fixed cause here student's info will be deleted. but it should be used only for disconnect from
        # teacher
        data = dict(request.args)

        delete_student = Students.query.filter_by(username=data['username']).first()
        delete_student.delete_from_db()

        os.remove(Students.create_picture_path(data['username']))
        return None


class GetInfo(Resource):

    @login_required
    def get(self):
        teacher_username = current_user.username
        students = Students.get_all_students(teacher_username)
        return make_response(render_template("showinfo.html", students=students))

    def put(self):
        print("in the put method, getinfo")
        print(request.method)


class Show(Resource):
    def get(self):
        students = Students.get_all_students("ehshan")
        return make_response(
            render_template("showinfo.html", students=students))
