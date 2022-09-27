from flask import Flask, render_template
from flask_restful import Api
from Resources import ReceiveInfo, GetInfo
import sys
import logging

app = Flask(__name__)
app.secret_key = "Arnob"
api = Api(app)


@app.route("/")
def home():
    return render_template("home.html")


api.add_resource(ReceiveInfo, "/form")
api.add_resource(GetInfo, "/showinfo")

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

if __name__ == '__main__':
    app.run(debug=True)