import csv
import random
from urls import urls
import json
import random
import sys
sys.path.append('/questions')

from flask import redirect, render_template, request, session
from functools import wraps
from urllib.request import Request, urlopen
from triviaroyale.categories import categories
from triviaroyale.urls import urls

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
    # get a random category id
    categoryids = [i for i in range(9,33)]
    randomid = random.choice(categoryids)

    # get category name using id in dict
    for categoryid in categories:
        if randomid == categoryid:
            pickedCategory = categories[categoryid]
        else:
            pass
    return pickedCategory

def getTrivia(categoryname):
    url = urls[categoryname]
    req = Request(url)
    r = urlopen(req).read()
    triviafile = json.loads(r.decode('utf-8'))
    print(triviafile)