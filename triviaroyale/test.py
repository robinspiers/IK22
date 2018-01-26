from urls import urls
import json
from urllib.request import Request, urlopen

url = urls["Art"]
req = Request(url)

r = urlopen(req).read()
triviafile = json.loads(r.decode('utf-8'))

# create variables
results = triviafile["results"][0]
question = results["question"]
correct_answer = results["correct_answer"]
incorrect_answer1 = results["incorrect_answers"][0]
incorrect_answer2 = results["incorrect_answers"][1]
incorrect_answer3 = results["incorrect_answers"][2]