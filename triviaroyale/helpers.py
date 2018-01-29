import csv
import random
import json
import random
import sys

from flask import redirect, render_template, request, session
from functools import wraps
from urllib.request import Request, urlopen
from categories import categories
from urls import urls

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
    """
    Get a random category id.
    """
    # choose random number
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
    return(triviafile)

def fixedquotes(s):
    for old, new in [("&quot;", "'"), ("&#039;", "'"), ("#ldquo;", "'"), ("#rdquo;", "'"), ("#lsquo;", "'"), ("#rsquo;", "'")]:
        s = s.replace(old, new)
    return s

def triviaItems(trivia):
    # create variables
    results = trivia["results"][0]
    question = fixedquotes(results["question"])
    correct_answer = fixedquotes(results["correct_answer"])
    incorrect_answer1 = fixedquotes(results["incorrect_answers"][0])
    incorrect_answer2 = fixedquotes(results["incorrect_answers"][1])
    incorrect_answer3 = fixedquotes(results["incorrect_answers"][2])
    return question, correct_answer, incorrect_answer1, incorrect_answer2, incorrect_answer3
