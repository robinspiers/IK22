
# voer dit in terminal bij toevoegen nieuwe table
# python3
# from application import db
# db.create_all()

from application import *

class User(db.Model):

    __tablename__ = "users"
    id = db.Column('user_id', db.Integer, primary_key=True)
    username = db.Column('username', db.Text)
    password = db.Column('password', db.Text)

    def __init__(self, username, password):
        self.username = username
        self.password = pwd_context.hash(password)

