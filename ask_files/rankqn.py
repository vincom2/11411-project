import re

pronouns = ['he', 'him', 'she', 'her', 'they', 'them', 'that', 'this']

def score(question):
    score = 0
    # score += len(question) # this did not work out
    regex = re.compile(r'.*\b(?:%s)\b' % '|'.join(pronouns))
    if regex.match(question.lower()):
        # print "BAD:", question
        score -= 1000
    return score