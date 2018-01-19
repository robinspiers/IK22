from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp

from helpers import *

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///triviaroyale.db")

@app.route("/login", methods = ["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # "POST" method
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("Must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("Must provide password")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", \
                          username = request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("Invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return redirect(url_for("index"))

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

        # require user to submit the same password again
        elif request.form.get("password") != request.form.get("password2"):
            return apology("Submitted passwords are not identical")

        # insert new user into users, store hash of the password
        new_user = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)", \
                             username = request.form.get("username"), \
                             hash = pwd_context.hash(request.form.get("password")))

        # ensure username does not already exist
        if not new_user:
            return apology("Username already exists")

        # keep user logged in
        session["user_id"] = new_user

        # redirect to homepage
        return redirect(url_for("index"))

    # "GET" method
    else:
        return render_template("register.html")