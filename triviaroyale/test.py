answerdict = {}
if Results.query.get(1).correct_answer == Results.query.get(1).answer1:
    answerdict.append("answer1" : Results.query.get(1).correct_answer)
elif Results.query.get(1).correct_answer == Results.query.get(1).answer2:
    answerdict.append("answer2" : Results.query.get(1).correct_answer)
elif Results.query.get(1).correct_answer == Results.query.get(1).answer3:
    answerdict.append("answer3" : Results.query.get(1).correct_answer)
elif Results.query.get(1).correct_answer == Results.query.get(1).answer4:
    answerdict.append("answer4" : Results.query.get(1).correct_answer)