
# voer dit in terminal bij toevoegen nieuwe table
# python3
# from application import db
# db.create_all()
# gebruikte bronnen https://blog.openshift.com/use-flask-login-to-add-user-authentication-to-your-python-application/
# https://flask-login.readthedocs.io/en/latest/#flask_login.login_user

from application import *

class User(db.Model):

    __tablename__ = "users"
    id = db.Column('user_id', db.Integer, primary_key=True)
    username = db.Column('username', db.Text, unique=True, index=True)
    password = db.Column('password', db.Text)
    highscore = db.Column('highscore', db.Integer)
    todos = db.relationship('Todo' , backref='user',lazy='dynamic')
    catergories = db.relationship('Categories', backref = 'user', lazy = 'dynamic')
    results = db.relationship('Results', backref = 'user', lazy = 'dynamic')


    def __init__(self, username, password, highscore):
        self.username = username
        self.password = pwd_context.hash(password)
        self.highscore = highscore

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

class Categories(db.Model):

    __tablename__ = "categories"
    id = db.Column('category_id', db.Integer, primary_key=True)
    firstcat = db.Column('firstcat', db.Text)
    secondcat = db.Column('secondcat', db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    def __init__(self, firstcat, secondcat):
        self.firstcat = firstcat
        self.secondcat = secondcat

class Results(db.Model):
    __tablename__ = "results"
    id = db.Column('result_id', db.Integer, primary_key=True)
    question = db.Column('question', db.Text)
    correct_answer = db.Column('correct_answer', db.Text)
    incorrect_answer1 = db.Column('incorrect_answer1', db.Text)
    incorrect_answer2 = db.Column('incorrect_answer2', db.Text)
    incorrect_answer3 = db.Column('incorrect_answer3', db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    def __init__(self, question, correct_answer, incorrect_answer1, incorrect_answer2, incorrect_answer3):
        self.correct_answer = correct_answer
        self.question = question
        self.incorrect_answer1 = incorrect_answer1
        self.incorrect_answer2 = incorrect_answer2
        self.incorrect_answer3 = incorrect_answer3

class Choice(db.Model):
    __tablename__ = "choice"
    id = db.Column('choice_id', db.Integer, primary_key=True)
    choice = db.Column('choice', db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'))

    def __init__(self, category):
        self.choice = choice








