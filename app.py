from flask import Flask, render_template
from flask_restful import Api
from Resources import Home, ReceiveInfo, GetInfo, Show
from profile import Profile

app = Flask(__name__)
app.secret_key = "Arnob"
api = Api(app)


api.add_resource(Home, "/")
api.add_resource(ReceiveInfo, "/form")
api.add_resource(GetInfo, "/showinfo")
api.add_resource(Profile, "/<string:name>")
api.add_resource(Show, "/show")
if __name__ == '__main__':
    app.run(debug=False)