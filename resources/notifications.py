from flask import request, make_response, render_template, redirect, url_for, flash
from flask_restful import Resource
from flask_login import current_user

from models.notifications import Notifications


class Notify(Resource):
    def get(self):
        notifications = (Notifications.query.with_entities(Notifications.question_id, Notifications.question,
                                                           Notifications.sender, Notifications.receiver,
                                                           Notifications.status)
                         .filter_by(receiver=current_user.username).all())
        if notifications:
            notifications.reverse()
            return make_response(render_template("notifications.html", notifications=notifications,
                                                 notify=Notifications.pending()))
        else:
            flash("You have no notification.")
            return make_response(render_template("message.html"))
