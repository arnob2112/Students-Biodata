from flask import Flask, render_template
from flask_restful import Api
from Resources import Home, ReceiveInfo, GetInfo

app = Flask(__name__)
app.secret_key = "Arnob"
api = Api(app)


api.add_resource(Home, "/")
api.add_resource(ReceiveInfo, "/form")
api.add_resource(GetInfo, "/showinfo")

if __name__ == '__main__':
    app.run(debug=True)