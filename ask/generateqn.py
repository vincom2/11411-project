"""obviously this doesn't actually do anything yet
   I just feel like this would be a good way to organise stuff
   WOOHOO 2 FUNCTIONS"""

import generic
import classify
import re
import sys

def syntactic_inversion(blah):
    pass

def pick_sentences(blah):
    pass

# article: article filename
# also this should probably return them, not just print them, so we can pick and choose or something
# (assuming we ever get the proper question-generating part working...)
def make_generic_qns(article):
    category = classify.classify(article)
    # such efficiency, opening it twice...
    with open(article) as f:
        first_line = f.readline()
        name = re.match(r'(.*?)\s*\(', first_line)
        if name == None:
            name = first_line.rstrip('\n')
    generic_qns = generic.lookup[category]
    for qn in generic_qns:
        print qn.format(name)

# whoops, this was supposed to be in ask.py, not here
# but since nothing works yet, whatever
def main():
    if len(sys.argv) != 3:
        print "usage: ./generateqn.py <article>.txt nquestions"
        # yes, yes, it just disregards nquestions anyway
        sys.exit(1)

    make_generic_qns(sys.argv[1])

if __name__ == '__main__':
    main()
