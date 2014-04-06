#!/usr/bin/env python
"""obviously this doesn't actually do anything yet
   I just feel like this would be a good way to organise stuff
   WOOHOO 2 FUNCTIONS"""

import generic, classify
import re, sys
import nltk
import ner
import pattern.en as en
import jsonrpclib
from simplejson import loads

core = jsonrpclib.Server('http://localhost:8080')
nent = ner.SocketNER(host = 'localhost', port = 12345)
tparse = nltk.tree.ParentedTree.parse

ner_host = 'localhost'
ner_port = 12345

def qn_tense(word):
    return en.conjugate(word)

def who_questions(sentence, topic):
    topic_lower = topic.lower()
    s_rev = sentence.split(' ').reverse()
    want = [u'ORGANIZATION', u'PERSON']
    result = loads(core.parse(sentence))
    tree = tparse(result['sentences'][0]['parsetree'])
    entities = nent.get_entities(sentence)
    possibilities = []
    for w in want:
        if w in entities:
            for e in entities[w]:
                if e.lower() in topic_lower:
                    continue
                # ok, we've found a good NE. now locate it in the tree so we can extract the verb.
                ent = e.split(' ')
                for subtree in tree.subtrees():
                    words = subtree.leaves()
                    for i in xrange(len(ent)):
                        if i >= len(words) or words[i] != ent[i]:
                            continue
                        # good, we've found the subtree that contains our NE
                        parent = subtree.parent()
                        while parent.node != 'VP':
                            parent = parent.parent()
                        # now parent is the VP, I guess
                        # this is actually pretty bad. you should try and find a way to get the prepositions and shit too...
                        for thing in parent.subtrees():
                            if 'VB' in thing.node:
                                verb = thing.leaves()[0]
                                possibilities.append((e, verb, thing.node))

    questions = set() # I don't know why there are duplicates, but whatever
    for entity, verb, tense in possibilities:
        # did/does definitely doesn't work for everything. e.g. some verbs go with "is"
        # the "easiest" way I can think for this is to train some bigram/trigram model
        # on what kind of auxiliaries verbs occur with, but this requires data that I don't know where to get...
        if tense == 'VBD': # past tense
            aux = "Did"
        else:
            aux = "Does" # we're going to assume singular, whatever
        questions.add("Who {} {} {}?".format(aux.lower(), topic, qn_tense(verb)))
        questions.add("{} {} {} {}?".format(aux, topic, qn_tense(verb), entity))

    return list(questions)



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

# if __name__ == '__main__':
#     main()
