from flask import Flask, render_template
from flask_restful import Api
from Resources import ReceiveInfo, GetInfo

app = Flask(__name__)
app.secret_key = "Arnob"
api = Api(app)


@app.route("/")
def home():
    return render_template("home.html")


api.add_resource(ReceiveInfo, "/")
api.add_resource(GetInfo, "/showinfo")

if __name__ == '__main__':
    app.run(debug=True)