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
        notices = NoticeBoard.query.with_entities(NoticeBoard.notice, NoticeBoard.name, NoticeBoard.date).all()[::-1]

        return make_response(render_template("notice_board.html", notices=notices))

    def post(self):
        teacher_name = " ".join(Teachers.query.with_entities(Teachers.firstname, Teachers.lastname).
                                filter_by(username=current_user.username).first())
        notice = request.form.get('notice')
        date = datetime.now(timezone('Asia/Dhaka')).strftime("%I:%M %p - %d %B, %Y")
        new_notice = NoticeBoard(name=teacher_name, notice=notice, date=date)
        new_notice.save_to_db()
        return redirect(url_for("notice"))
