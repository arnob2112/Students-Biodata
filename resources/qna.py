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
            all_questions = QNA.query.with_entities(QNA.questions, QNA.answers, QNA.id, QNA.student_username).all()
            sorted_all_questions = []
            for questions in all_questions:
                qna = dict(zip_longest(questions[0], questions[1], fillvalue="Pending"))
                sorted_all_questions.append([qna, questions[2], questions[3]])
            sorted_all_questions.reverse()
            return make_response(render_template("qna.html", all_questions=sorted_all_questions,
                                                 notify=Notifications.pending()))
        elif variable.lower() == "new_question":
            return make_response(render_template("ask_question.html", notify=Notifications.pending()))
        else:
            flash("Error happened. Please try again")
            return make_response(render_template("message.html"))

    @login_required
    def post(self, variable):
        data = dict(request.form.items())
        question_id = data.get("question_id")
        new_question = data.get("new_question")

        if current_user.job.lower() == "student":
            if question_id:
                questions_object = QNA.query.filter_by(id=question_id).first()
                try:
                    questions = [*questions_object.questions]
                except:
                    questions = []
                questions.append(new_question)
                questions_object.questions = questions
                questions_object.status = "Pending"
                questions_object.save_to_db()

                # making notification for teacher
                notification = Notifications.query.filter_by(question_id=question_id,
                                                             receiver=current_user.username).first()
                if notification:
                    notification.sender, notification.receiver = notification.receiver, notification.sender
                    notification.status = "pending"
                    print("I am in teacher notification", "sen", notification.sender, "rec", notification.receiver)
                    notification.save_to_db()

                return redirect(url_for("answer", question_id=question_id))
            else:
                new_question_object = QNA(questions=[new_question], answers=[],
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
                try:
                    answers = [*question_object.answers]
                except:
                    answers = []

                answers.append(new_answer)
                # print("answers", answers)
                question_object.answers = answers
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
