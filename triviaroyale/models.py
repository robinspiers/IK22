from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp

from helpers import *

# configure application
app = Flask(__name__)

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///triviaroyale.db")

# query database for username
def find_user(username, password):
    rows = db.execute("SELECT * FROM users WHERE username = :username", username = username)
    if len(rows) != 1 or not pwd_context.verify(password, rows[0]["hash"]):
        return apology("Invalid username and/or password")
    else:
        return rows

# remember which user is logged in
def keepLoggedIn(username):
    rows = db.execute("SELECT * FROM users WHERE username = :username", username = username)
    return rows[0]["id"]

# insert new user into users, store hash of the password
def insert_user(username, password):
    new_user = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)", \
                          username = username, hash = pwd_context.hash(password))
    if not new_user:
        return apology("Username already exists")
    else:
        return new_user
