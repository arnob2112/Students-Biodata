from flask import redirect, url_for, flash, session
from flask_restful import Resource
from smtplib import SMTP
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

sender_email = "ehshanulhq@gmail.com"
password = "urfmabihxymkssds"

serializer = URLSafeTimedSerializer("Arnob")


def verify_mail(receiver_email):
    server = SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, password)

    token = serializer.dumps(receiver_email, salt='email-confirm')
    link = url_for('emailverification', token=token, _external=True)

    message = f"Subject: Verify your email \nFrom: {sender_email}\nTo: {receiver_email}\n" \
              f"Content-Type: text/html\n\n{link}"
    server.sendmail(sender_email, receiver_email, message)


class EmailVerification(Resource):

    def get(self, token):
        try:
            print("in email post")
            email = serializer.loads(token, salt='email-confirm', max_age=3600)
            print('verify email', email)
        except SignatureExpired:
            return '<h1> The token is expired! </h1>'
        session['_flashes'].clear()
        flash("Your email has verified. Thank you.")
        return redirect(url_for('home'))
