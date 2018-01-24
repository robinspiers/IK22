
# voer dit in terminal bij toevoegen nieuwe table
# python3
# from application import db
# db.create_all()
# gebruikte bronnen https://blog.openshift.com/use-flask-login-to-add-user-authentication-to-your-python-application/
# https://flask-login.readthedocs.io/en/latest/#flask_login.login_user

from triviaroyale.application import *

class User(db.Model):

    __tablename__ = "users"
    id = db.Column('user_id', db.Integer, primary_key=True)
    username = db.Column('username', db.Text, unique=True, index=True)
    password = db.Column('password', db.Text)
    todos = db.relationship('Todo' , backref='user',lazy='dynamic')

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
        unicode = str
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.username)

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column('todo_id', db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

class Categories1(db.Model):

        __tablename__ = "category1"
        name = db.Column(categories[category1], db.Text)
        number = db.Column('category1', db.Integer)

      def __init__(self, name, number):
        self.name = name
        self.number = number



