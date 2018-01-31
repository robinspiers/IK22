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

def randomcategory():
    """Choose a random category."""
    # choose a random category id
    categoryids = [i for i in range(9,33)]
    randomid = random.choice(categoryids)

    # get category name from dict using id as key
    for categoryid in categories:
        if randomid == categoryid:
            pickedCategory = categories[categoryid]
        else:
            pass
    return pickedCategory

def getTrivia(categoryname):
    """Download .json package from online triviadatabase."""
    url = urls[categoryname]
    req = Request(url)
    r = urlopen(req).read()
    triviafile = json.loads(r.decode('utf-8'))
    return(triviafile)

def fixedsymbols(s):
    for old, new in [("&quot;", "'"), ("&#039;", "'"), ("#ldquo;", "'"), ("#rdquo;", "'"), ("#lsquo;", "'"), \
                    ("#rsquo;", "'"), ("&amp;", "&"), ("&lt;", "<"), ("&rt;", ">")]:
        s = s.replace(old, new)
    return s

def triviaItems(trivia):
    """Create usable variables."""
    results = trivia["results"][0]
    question = fixedsymbols(results["question"])
    correct_answer = fixedsymbols(results["correct_answer"])
    incorrect_answer1 = fixedsymbols(results["incorrect_answers"][0])
    incorrect_answer2 = fixedsymbols(results["incorrect_answers"][1])
    incorrect_answer3 = fixedsymbols(results["incorrect_answers"][2])
    return question, correct_answer, incorrect_answer1, incorrect_answer2, incorrect_answer3

def shuffle(answer1, answer2, answer3, answer4):
    """Shuffles the four answers."""
    answers = [answer1, answer2, answer3, answer4]
    random.shuffle(answers)
    return answers[0], answers[1], answers[2], answers[3]