from flask import request, render_template, make_response, redirect, url_for
from flask_restful import Resource
from flask_login import current_user
from datetime import datetime
from pytz import timezone

from models.students import Students
from models.notice_board import NoticeBoard
from models.teachers import Teachers


class Notice(Resource):

    def get(self):
        # if current_user.is_authenticated:
        #     teacher_name = " ".join(Students.query.with_entities(Students.firstname, Students.lastname)
        #                             .filter_by(job="Teacher", teacher_username=current_user.username).first())
        # else:
        #     teacher_name = None
        notices = NoticeBoard.query.with_entities(NoticeBoard.notice, NoticeBoard.name, NoticeBoard.date).all()[::-1]
        # if current_user.is_authenticated:
        #     student_usernames, teacher_username = Students.find_all_username(current_user.username)
        # else:
        #     student_usernames = None
        #     teacher_username = None

        return make_response(render_template("notice_board.html", notices=notices))

    def post(self):
        teacher_name = " ".join(Teachers.query.with_entities(Teachers.firstname, Teachers.lastname).
                                filter_by(username=current_user.username).first())
        notice = request.form.get('notice')
        # teacher_name = request.form.get('teacher_name')
        # date = datetime.now().strftime("%I:%M %p - %d %B, %Y")
        date = datetime.now(timezone('Asia/Dhaka')).strftime("%I:%M %p - %d %B, %Y")
        new_notice = NoticeBoard(name=teacher_name, notice=notice, date=date)
        new_notice.save_to_db()
        return redirect(url_for("notice"))
