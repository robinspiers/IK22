
# voer dit in terminal bij toevoegen nieuwe table
# python3
# from application import db
# db.create_all()

from application import *

class User(db.Model):

    __tablename__ = "users"
    id = db.Column('user_id', db.Integer, primary_key=True)
    username = db.Column('username', db.Text, unique=True, index=True)
    password = db.Column('password', db.Text)

    def __init__(self, username, password):
        self.username = username
        self.password = pwd_context.hash(password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.username)
