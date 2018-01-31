from cs50 import SQL
from flask import Flask, g, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_login import login_user , logout_user , current_user , login_required

from helpers import *

# configure application
app = Flask(__name__)

# Flask-SQLAlchemy
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///triviaroyale.db"
app.config["SQLALCHEMY_ECHO"] = True
db = SQLAlchemy(app)

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# initialize LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# import classes from models.py
from models import User
from models import Categories
from models import Results
from models import Choice

# ensure responses are not cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# load user from an id
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user

@app.route("/")
def index():
    """Homepage of the website, features the high scores leaderboard."""

    # order high scores from highest to lowest
    rows = User.query.order_by(User.highscore.desc())
    return render_template("index.html", users=rows)

@app.route("/login", methods = ["GET", "POST"])
def login():
    """Log user in."""

    # "GET" method
    if request.method == "GET":
        return render_template("login.html")

    # "POST" method
    else:

        # require user to submit username
        if not request.form["username"]:
            flash("Must provide username", "warning")
            return render_template("login.html")

        # require user to submit password
        elif not request.form["password"]:
            flash("Must provide password", "warning")
            return render_template("login.html")

        # create variables
        username = request.form["username"]
        password = request.form["password"]

        # search user in the database, check if username and password are correct
        registered_user = User.query.filter_by(username=username).first()

        if registered_user is None:
            flash("Username is invalid" , "warning")
            return render_template("login.html")

        if not pwd_context.verify(password, registered_user.password):
            flash("Password is invalid" , "warning")
            return render_template("login.html")

        # keep user logged in
        login_user(registered_user)
        flash("Logged in successfully", "info")
        return redirect(url_for("index"))

@app.route("/logout")
def logout():
    """Log user out."""

    User.query.get(current_user.id).currentscore = 0
    db.session.commit()
    logout_user()
    flash("Logged out successfully", "info")
    return redirect(url_for("index"))

@app.route("/register", methods = ["GET", "POST"])
def register():
    """Register user."""

    # "GET" method
    if request.method == "GET":
        return render_template("register.html")

    # "POST" method
    else:

        # require user to submit username
        if not request.form["username"]:
            flash("Must provide username", "warning")
            return render_template("register.html")

        # require user to submit password
        elif not request.form["password"]:
            flash("Must provide password", "warning")
            return render_template("register.html")

        # require user to submit password again
        elif not request.form["password2"]:
            flash("Must provide password again", "warning")
            return render_template("register.html")

        # require user to submit identical passwords
        elif request.form["password"] != request.form["password2"]:
            flash("Submitted passwords are not identical", "warning")
            return render_template("register.html")

        # add user to database
        user = User(request.form["username"], request.form["password"], 0, 0)
        db.session.add(user)
        db.session.commit()
        flash("User successfully registered", "info")

        # redirect to login page
        return redirect(url_for("login"))

@app.route("/pregame", methods = ["GET", "POST"])
def pregame():
    """Let the user choose one out of two random categories."""

    # "GET" method
    if request.method == "GET":

        # if table is empty, insert values
        if Categories.query.get(1) is None:

            # generate two different random categories
            firstcat = randomcategory()
            secondcat = randomcategory()
            while firstcat == secondcat:
                secondcat = randomcategory()

            # update database with new categories
            randomcats = Categories(firstcat, secondcat)
            db.session.add(randomcats)
            db.session.commit()

        # update the table otherwise
        else:

            # generate two different random categories
            Categories.query.get(1).firstcat = randomcategory()
            Categories.query.get(1).secondcat = randomcategory()
            while Categories.query.get(1).firstcat == Categories.query.get(1).secondcat:
                Categories.query.get(1).secondcat = randomcategory()
            db.session.commit()

        # query for categories
        cats = Categories.query.get(1)
        return render_template("pregame.html", cats=cats)

    # "POST" method
    else:

        # if the first category was chosen
        if request.form.get("cat") == "1":
            if Choice.query.get(1) is None:
                keuze = Choice(Categories.query.get(1).firstcat)
                db.session.add(keuze)
                db.session.commit()
            Choice.query.get(1).choice = Categories.query.get(1).firstcat
            db.session.commit()
            return redirect(url_for("question"))

        # if the second category was chosen
        if request.form.get("cat") == "2":
            if Choice.query.get(1) is None:
                keuze = Choice(Categories.query.get(1).secondcat)
                db.session.add(keuze)
                db.session.commit()
            Choice.query.get(1).choice = Categories.query.get(1).secondcat
            db.session.commit()
            return redirect(url_for("question"))

@app.route("/question", methods = ["GET", "POST"])
def question():
    """Let the user answer the trivia question."""

    # "GET" method
    if request.method == "GET":

        # get trivia file from online API
        triviafile = getTrivia(Choice.query.get(1).choice)

        # create variables
        question, correct_answer, incorrect_answer1, incorrect_answer2, incorrect_answer3 = triviaItems(triviafile)

        # create shuffable variables for db
        answer1, answer2, answer3, answer4 = shuffle(correct_answer, incorrect_answer1, incorrect_answer2, incorrect_answer3)

        # if table is empty, insert values
        if Results.query.get(1) is None:

            # store question and answers into database
            result = Results(question, answer1, answer2, answer3, answer4, correct_answer)
            db.session.add(result)
            db.session.commit()

        # update the table otherwise
        else:
            Results.query.get(1).question = question
            Results.query.get(1).answer1 = answer1
            Results.query.get(1).answer2 = answer2
            Results.query.get(1).answer3 = answer3
            Results.query.get(1).answer4 = answer4
            Results.query.get(1).correct_answer = correct_answer
            db.session.commit()

        # query for question and results
        trivia = Results.query.get(1)
        return render_template('question.html', trivia=trivia)

    # "POST" method
    else:

        # create dictionary with correct answer and incorrect answers
        answerdict = {"answer1" : "incorrect", "answer2" : "incorrect", "answer3" : "incorrect", "answer4" : "incorrect"}
        if Results.query.get(1).correct_answer == Results.query.get(1).answer1:
            answerdict["answer1"] = "correct"
        elif Results.query.get(1).correct_answer == Results.query.get(1).answer2:
            answerdict["answer2"] = "correct"
        elif Results.query.get(1).correct_answer == Results.query.get(1).answer3:
            answerdict["answer3"] = "correct"
        elif Results.query.get(1).correct_answer == Results.query.get(1).answer4:
            answerdict["answer4"] = "correct"

        # if user is not logged in
        if session.get("user_id") == None:

            # correct answer
            if answerdict[request.form.get("answer")] == "correct":
                flash("Answer is correct!", "success")
                return redirect(url_for("proceed"))

            # incorrect answer
            else:
                flash("Answer is wrong!", "danger")
                return redirect(url_for("proceed"))

        # if user is logged in
        else:

            # correct answer
            if answerdict[request.form.get("answer")] == "correct":
                flash("Answer is correct! You have earned 10 points!", "success")

                # add 10 points to user's current score
                User.query.get(current_user.id).currentscore += 10

                # update high score if broken
                if User.query.get(current_user.id).currentscore > User.query.get(current_user.id).highscore:
                    User.query.get(current_user.id).highscore += 10

                db.session.commit()
                return redirect(url_for("proceed_online"))

            # incorrect answer
            else:
                flash("Answer is wrong! Your score has been reset to 0.", "danger")

                # reset current score to 0
                User.query.get(current_user.id).currentscore = 0

                db.session.commit()
                return redirect(url_for("proceed_online"))

@app.route("/proceed", methods = ["GET", "POST"])
def proceed():
    """Allow the user to choose to continue or to stop playing."""

    # "GET" method
    if request.method == "GET":

        # show correct answer
        answer = Results.query.get(1).correct_answer
        return render_template("proceed.html", answer=answer)

    # "POST" method
    else:

        # if user wants to proceed
        if request.form.get("submit") == "yes":
            return redirect(url_from("pregame"))

        # if user wants to return to homepage
        elif request.form.get("submit") == "no":
            return redirect(url_from("index"))

@app.route("/proceed_online", methods = ["GET", "POST"])
def proceed_online():
    """Allow the logged in user to choose to continue or to stop playing. Also show the user's current score."""

    # "GET" method
    if request.method == "GET":

        # show correct answer
        answer = Results.query.get(1).correct_answer

        # show user's current score
        score = User.query.get(current_user.id).currentscore

        return render_template("proceed_online.html", score=score, answer=answer)

    # "POST" method
    else:

        # if user wants to proceed
        if request.form.get("submit") == "yes":
            return redirect(url_from("pregame"))

        # if user wants to return to homepage
        elif request.form.get("submit") == "no":
            return redirect(url_from("index"))