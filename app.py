from flask import Flask
from flask_restful import Api
from flask_login import LoginManager

from models.users import Users
from database import db
from resources.authentication import Signup, Login, Logout
from resources.email_verification import EmailVerification
from resources.access_info import Home, ReceiveInfo, GetInfo, Show
from resources.people import Profile, All, Connections, AddConnection
from resources.requests import ConnectionPending
from resources.notice_board import Notice
from resources.qna import Question, Answer

app = Flask(__name__)
app.secret_key = "Arnob"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///All Information.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


@login_manager.user_loader
def user_loader(user_id):
    return Users.query.get(int(user_id))


db.init_app(app)
with app.app_context():
    db.create_all()


api.add_resource(Home, "/")
api.add_resource(Signup, "/<string:job>/signup")
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(EmailVerification, "/confirm_email/<token>")
api.add_resource(ReceiveInfo, "/<string:job>/form")
api.add_resource(Profile, "/<string:job>/<string:username>")
api.add_resource(All, "/<string:username>/all/<string:job>")
api.add_resource(Connections, "/<string:job>/<string:username>/connections")
api.add_resource(AddConnection, "/<string:job>/<string:username>/add connection")
api.add_resource(ConnectionPending, "/<string:job>/<string:username>/requests")
api.add_resource(Notice, "/noticeboard")
api.add_resource(Question, '/qna/<string:variable>')
api.add_resource(Answer, '/qna/answer/<string:question_id>')
api.add_resource(GetInfo, "/showinfo")  # need to check
api.add_resource(Show, "/show")  # need to check


if __name__ == '__main__':
    app.run(port=5000, debug=True)
