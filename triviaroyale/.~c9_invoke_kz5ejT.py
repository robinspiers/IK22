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
login_manager.login_view = 'login'

from models import User
import questions
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

@app.before_request
def before_request():
    g.user = current_user

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods = ["GET", "POST"])
def login():

    # 'GET' method
    if request.method == 'GET':
        return render_template('login.html')
    # "POST" method
    username = request.form['username']
    password = request.form['password']
    remember_me = False
    if 'remember_me' in request.form:
        remember_me = True

    # opzoeken van gebruiker in Database, waarbij username/password in db gelijk moet zijn aan ingevulde username/password
    registered_user = User.query.filter_by(username=username).first()
    if registered_user is None:
        flash('Username is invalid' , 'error')
    if not pwd_context.verify(password, registered_user.password):
        flash('Password is invalid' , 'error')
        return redirect(url_for('login'))
    # gebruiker inloggen omdat hij in database staat
    login_user(registered_user, remember = remember_me)
    flash('Logged in successfully')
    return redirect(request.args.get('next') or url_for('index'))

@app.route("/logout")
def logout():
    """Log user out."""
    logout_user()
    # redirect user to login form
    return redirect(url_for("index"))

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
        # toevoegen van user aan Database
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

