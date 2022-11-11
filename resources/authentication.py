from flask import request, render_template, make_response, url_for, redirect, flash
from flask_restful import Resource
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user

from models.users import Users
from database import db


class Login(Resource):
    def get(self):
        return make_response(render_template('login.html'))

    def post(self):
        username = request.form.get('username')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = Users.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            flash("Please check your details and try again.")
            print("wrong user")
            return redirect(url_for('login'))

        login_user(user, remember=remember)
        return redirect(url_for('home'))


class Signup(Resource):
    TABLE_NAME = 'user'

    def get(self):
        return make_response(render_template('signup.html'))

    def post(self):
        username = request.form.get('username')
        password = request.form.get('password')

        user = Users.query.filter_by(username=username).first()
        if user:
            flash("Username has already exists! Try again. ")
            print("user exists")
            return redirect(url_for('signup'))

        new_user = Users(username=username, password=generate_password_hash(password, method='sha256'))
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        return redirect(url_for('home'))


class Logout(Resource):
    @login_required
    def get(self):
        logout_user()
        return redirect(url_for('home'))
