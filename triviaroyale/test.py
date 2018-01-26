import random
from categories import categories

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

firstcat = randomcategory()
secondcat = randomcategory()
while firstcat == secondcat:
    secondcat = random.category()
print(firstcat,secondcat)