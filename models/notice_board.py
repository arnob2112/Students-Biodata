from database import db


class NoticeBoard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    notice = db.Column(db.String)
    date = db.Column(db.String)

    def __int__(self, name, notice, date):
        self.name = name
        self.notice = notice
        self.date = date

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()