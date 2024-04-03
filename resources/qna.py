from flask import make_response, render_template, request, flash, redirect, url_for
from flask_restful import Resource
from flask_login import login_required, current_user
from itertools import zip_longest

from models.qna import QNA
from models.notifications import Notifications


class Question(Resource):
    @login_required
    def get(self, variable):
        if variable.lower() == "all":
            all_questions = QNA.all_questions()
            return make_response(render_template("qna.html", all_questions=all_questions,
                                                 notify=Notifications.pending()))
        elif variable.lower() == "new_question":
            return make_response(render_template("ask_question.html", notify=Notifications.pending()))
        elif variable.lower() == "my_questions":
            my_questions = QNA.my_questions()
            return make_response(render_template("qna.html", all_questions=my_questions,
                                                 notify=Notifications.pending()))
        else:
            flash("Error happened. Please try again")
            return make_response(render_template("message.html"))

    @login_required
    def post(self, variable):
        data = dict(request.form.items())
        question_id = data.get("question_id")
        new_question = data.get("new_question")
        # question_picture = request.files.get("question_picture")
        # audio = request.files.get("audio")

        if current_user.job.lower() == "student":
            if question_id:
                questions_object = QNA.query.filter_by(id=question_id).first()
                # sudhu prothom bar er picture/audio er jnn path banano hoiche. but porer picture/audio er path banano
                # hoy nai.
                # sudhu previous question e picture/audio save korar logic ready hoiche. but new question e text e
                # question naki audio naki picture eta alada kore then alada vabe jayga moto database e inpur dite hbe.
                # audio and picture save check kora hoy nai.
                # audio and picture save korar process ta ekta function e niye gele bhalo hbe.

                # if audio:
                #     new_audio_path = QNA.create_audio_path()
                #     questions_object.audio_path = [*questions_object.audio_path, new_audio_path]
                #     audio.save(new_audio_path)
                #     questions_object.save_to_db()
                # elif question_picture:
                #     new_picture_path = QNA.create_picture_path()
                #     questions_object.picture_path = [*questions_object.picture_path, new_picture_path]
                #     question_picture.save(new_picture_path)
                #     questions_object.save_to_db()

                # else:
                questions_object.questions = [*questions_object.questions, new_question]
                questions_object.status = "Pending"
                questions_object.save_to_db()

                # making notification for teacher
                notification = Notifications.query.filter_by(question_id=question_id,
                                                             receiver=current_user.username).first()
                if notification:
                    notification.sender, notification.receiver = notification.receiver, notification.sender
                    notification.status = "pending"
                    notification.save_to_db()

                return redirect(url_for("answer", question_id=question_id))
            else:
                new_question_object = QNA(questions=[new_question], answers=[], picture_path=[], audio_path=[],
                                          student_username=current_user.username, status="Pending")
                new_question_object.save_to_db()
                return redirect(url_for("question", variable="all"))
        else:
            flash("You are not a student. Please try again")
            return make_response(render_template("message.html"))


class Answer(Resource):
    @login_required
    def get(self, question_id):
        question_object = QNA.query.filter_by(id=question_id).first()
        qna = dict(zip_longest(question_object.questions, question_object.answers, fillvalue="Pending"))

        # marking notification as seen
        notification = Notifications.query.filter_by(question_id=question_id, receiver=current_user.username).first()
        if notification and current_user.username == notification.receiver:
            notification.status = "seen"
            notification.save_to_db()

        return make_response(render_template("question.html", qna=qna, question_id=question_id,
                                             username=question_object.student_username, status=question_object.status,
                                             notify=Notifications.pending()))

    @login_required
    def post(self, question_id):
        data = dict(request.form.items())
        question_id = data.get("question_id")
        new_answer = data.get("new_answer")

        if current_user.job.lower() == "teacher":
            if question_id:
                question_object = QNA.query.filter_by(id=question_id).first()
                # print("answers", answers)
                question_object.answers = [*question_object.answers, new_answer]
                question_object.status = "Done"
                question_object.save_to_db()

                # making notification for student
                notification = Notifications.query.filter_by(question_id=question_id,
                                                             receiver=current_user.username).first()
                if notification:
                    notification.sender, notification.receiver = notification.receiver, notification.sender
                    notification.status = "pending"
                else:
                    notification = Notifications(question_id=question_id, question=question_object.questions[0],
                                                 sender=current_user.username,
                                                 receiver=question_object.student_username, status="pending")
                notification.save_to_db()

                return redirect(url_for("answer", question_id=question_id))
        else:
            flash("You are not a teacher. Please try again")
            return make_response(render_template("message.html"))
