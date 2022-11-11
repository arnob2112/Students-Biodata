from flask import Flask
from flask_restful import Api
from flask_login import LoginManager

from models.users import Users
from database import db
from resources.access_info import Home, ReceiveInfo, GetInfo, Show
from resources.Profile import Profile
from resources.authentication import Signup, Login, Logout
from resources.notice_board import Notice


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


@app.before_first_request
def create_table():
    with app.app_context():
        db.create_all()


#     db.create_all()
#     db.session.commit()


api.add_resource(Home, "/")
api.add_resource(Signup, "/signup")
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(ReceiveInfo, "/form")
api.add_resource(GetInfo, "/showinfo")
api.add_resource(Profile, "/<string:job>/<string:username>")
api.add_resource(Notice, "/noticeboard")
api.add_resource(Show, "/show")


if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
