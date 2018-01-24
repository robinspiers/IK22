from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
from flask_sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

from helpers import *

# configure application
app = Flask(__name__)

# Flask-SQLAlchemy
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///triviaroyale.db"
app.config["SQLALCHEMY_ECHO"] = True
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from models import User

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# load user from an id.
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods = ["GET", "POST"])
def login():
    """Log user in."""

    # "GET" method
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))

@app.route("/register", methods = ["GET", "POST"])
def register():
    """Register user."""

    # "POST" method
    if request.method == "POST":

        # require user to submit username
        if not request.form["username"]:
            return apology("Must provide username")

        # require user to submit password
        elif not request.form["password"]:
            return apology("Must provide password")

        elif not request.form["password2"]:
            return apology("Provide same password again")

        # require user to submit the same password again
        elif request.form["password"] != request.form["password2"]:
            return apology("Submitted passwords are not identical")

        user = User(request.form['username'] , request.form['password'])
        db.session.add(user)
        db.session.commit()
        flash('User successfully registered')

        # redirect to homepage
        return redirect(url_for('login'))

    # "GET" method
    else:
        return render_template("register.html")

@app.route("/pregame", methods = ["GET", "POST"])
def pregame():

    # "POST" method
    if request.method == "POST":
        return redirect(url_for("question"))

    # "GET" method
    else:
        return render_template("pregame.html")
