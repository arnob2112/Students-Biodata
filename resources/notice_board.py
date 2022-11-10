from flask import request, render_template, make_response, redirect, url_for
from flask_restful import Resource
from flask_login import current_user
from datetime import datetime

from models.students import Students
from models.notice_board import NoticeBoard


class Notice(Resource):

    def get(self):
        if current_user.is_authenticated:
            teacher_name = " ".join(Students.query.with_entities(Students.Firstname, Students.Lastname)
                                    .filter_by(Job="Teacher", Teacher_Username=current_user.username).first())
        else:
            teacher_name = None
        notices = NoticeBoard.query.with_entities(NoticeBoard.notice, NoticeBoard.name, NoticeBoard.date).all()[::-1]
        if current_user.is_authenticated:
            student_usernames, teacher_username = Students.find_all_username(current_user.username)
        else:
            student_usernames = None
            teacher_username = None

        return make_response(render_template("notice_board.html", notices=notices, teacher_name=teacher_name,
                                             student_usernames=student_usernames, teacher_username=teacher_username))

    def post(self):
        notice = request.form.get('notice')
        teacher_name = request.form.get('teacher_name')
        date = datetime.now().strftime("%I:%M %p - %d %B, %Y")
        new_notice = NoticeBoard(name=teacher_name, notice=notice, date=date)
        new_notice.save_to_db()
        return redirect(url_for("notice"))
