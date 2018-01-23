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

    # forget any user_id
    #session.clear()

    # "POST" method
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("Must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("Must provide password")

       # ensure username exists and password is correct
        #if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            #return apology("Invalid username and/or password")

        # remember which user has logged in
       #session["user_id"] = rows[0]["id"]

        # redirect user to home page
       # return redirect(url_for("index"))

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
        if not request.form.get("username"):
            return apology("Must provide username")

        # require user to submit password
        elif not request.form.get("password"):
            return apology("Must provide password")

        elif not request.form.get("password2"):
            return apology("Provide same password again")

        # require user to submit the same password again
        elif request.form.get("password") != request.form.get("password2"):
            return apology("Submitted passwords are not identical")

        registrant = Registrant(username = request.form["username"], password = request.form["password"])
        db.session.add(registrant)
        db.session.commit()
        # redirect to homepage
        return redirect(url_for("index"))

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
