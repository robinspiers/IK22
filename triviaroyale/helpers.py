import csv
import random
import urllib.request
import json
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

"""url = 'https://opentdb.com/api.php?amount=50&category=23&type=multiple'
req = urllib.request.Request(url)

# url lezen en decoden voor gebruik
r = urllib.request.urlopen(req).read()
cont = json.loads(r.decode('utf-8'))
counter = 0"""