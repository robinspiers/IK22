import csv
import urllib.request
import random
import sys
sys.path.append('/questions')

from triviaroyale.questions import categories
from flask import redirect, render_template, request, session
from functools import wraps


def apology(message, code=400):
    """Renders message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def randomcategory():
    # momenteel wordt er willekeurig 1 categorie uitgekozen voor in de url
    categories_list = [i for i in range(9,33)]
    options = random.choice(categories_list)
    return options

def trivia(number):
    return "https://opentdb.com/api.php?amount=1&category={{ number }}&type=multiple"