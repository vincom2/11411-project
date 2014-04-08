#!/usr/bin/env python

"""from current test output, it seems very important to be able to extract subjects. while it also
   seems very stupid to keep throwing external libraries at this because it's too hard to parse the output
   of external libraries already being used (e.g. corenlp-python), I think a good way to extract subjects might be
   https://github.com/knowitall/reverb/ """

import generic, classify
import re, codecs
import nltk, ner
import pattern.en as en
import jsonrpclib
from simplejson import loads
from sklearn.externals import joblib
from collections import defaultdict
import argparse

# commandline arguments
parser = argparse.ArgumentParser()
parser.add_argument("article", help="article to generate questions based on")
parser.add_argument("nquestions", help="number of questions to generate", type=int)
parser.add_argument("--corenlp-port", help="port that python-coreNLP server is listening on", default="12345")
parser.add_argument("--ner-port", help="port that NER server is listening on", type=int, default=12346)
parser.add_argument("--hostname", help="host that both servers are running on", default="localhost")

args = parser.parse_args()

core = jsonrpclib.Server('http://' + args.hostname + ':' + args.corenlp_port)
nent = ner.SocketNER(host = args.hostname, port = args.ner_port)
tparse = nltk.tree.ParentedTree.parse



def other_questions(result, n, topic):
    """replace this if you ever figure out how to generate the remaining types of questions"""
    return []

def qn_tense(word):
    return en.conjugate(word)

def replace_corefs(phrase, core_parse, n):
    """very terrible; assumes a coref only occurs once in a sentence, for instance"""
    corefs = core_parse[u'coref']
    for c in corefs:
        if len(c) > 1:
            temp = c[:-1]
        else:
            temp = [c]
        for e in temp: # I have no idea why some of the lists are nested...
            for d in e:
                # print phrase
                # print d[0][0]
                if phrase == d[0][0] and n == d[0][1]:
                    return d[-1][0]
    return phrase
    # for c in corefs:
    #     if len(c) > 1:
    #         temp = c[0]
    #     else:
    #         temp = c
    #     replace_with = temp[-1]

def locate_verb(ent, tree):
    # find subtree that contains the NE
    for subtree in tree.subtrees():
        words = subtree.leaves()
        for i in xrange(len(ent)):
            if i >= len(words) or words[i] != ent[i]:
                continue
            # good, we've found the subtree that contains our NE
            parent = subtree.parent()
            found_verb = False # if we find the verb now, our NE is the object, probably
            while parent != None and parent.node != 'VP':
                parent = parent.parent()
            # now parent is the VP if it's not None
            if parent != None:
                for thing in parent.subtrees():
                    if 'VB' in thing.node:
                        verb = thing.leaves()[0]
                        found_verb = True
                        # extract the preposition, if any, in a terrible way
                        find_prep = thing.right_sibling()
                        for st in find_prep.subtrees():
                            if st.node == 'IN' or st.node == 'RP':
                                prep = ' ' + st.leaves()[0]
                                break
                            else:
                                prep = ''
                        return verb, prep, thing.node, found_verb
            # didn't manage to find a parent VP; our NE is probably the subject            
            if not found_verb:
                curr = subtree.right_sibling()
                while curr != None and curr.node != 'VP':
                    curr = curr.right_sibling()
                if curr != None:
                    for thing in curr.subtrees():
                        if 'VB' in thing.node:
                            verb = thing.leaves()[0]
                            # extract preposition, if any
                            find_prep = thing.right_sibling()
                            if find_prep == None:
                                return None, None, None, None
                            for st in find_prep.subtrees():
                                if st.node == 'IN' or st.node == 'RP':
                                    prep = ' ' + st.leaves()[0]
                                    break
                                else:
                                    prep = ''
                            return verb, prep, thing.node, found_verb
    # somehow could not find anything
    return None, None, None, None


# actually, this isn't how you want to structure it. since each sentence is classified into question types separately,
# you want to pass in only the sentence instead of the whole text. but you also want the sentence number and
# the full coreNLP parse results, which should be done in a big wrapper function that also
# calls the classifier and shit.
def who_questions(result, n, topic):
    sentence = result['sentences'][n]
    tree = tparse(sentence['parsetree'])
    topic_lower = topic.lower()
    want = [u'ORGANIZATION', u'PERSON']
    # this is flawed, because if we managed to replace corefs with their referents first,
    # we'd probably end up with more entities identified. but oh well. 2hrd.
    entities = nent.get_entities(sentence['text'])
    possibilities = []

    for w in want:
        if w in entities:
            for tmp in entities[w]:
                e = replace_corefs(tmp, result, n)
                if e.lower() in topic_lower:
                    continue
                # ok, we've found a good NE. now locate it in the tree so we can extract the verb.
                verb, prep, tense, obj = locate_verb(e.split(' '), tree)
                if verb != None:
                    possibilities.append((e, verb, prep, tense, obj))
    
    questions = set() # I don't know why there are duplicates, but whatever
    # so now if found_verb is False, that means our NE is the subject
    for entity, verb, prep, tense, obj in possibilities:
        # did/does definitely doesn't work for everything. e.g. some verbs go with "is"
        # the "easiest" way I can think for this is to train some bigram/trigram model
        # on what kind of auxiliaries verbs occur with, but this requires data that I don't know where to get...
        # see, we should do proper subject-auxiliary inversion here, but I dunno how
        if tense == 'VBD': # past tense
            aux = "Did"
        else:
            aux = "Does" # we're going to assume singular, whatever
        if obj:
            questions.add(u"Who {} {} {}{}?".format(aux.lower(), topic, qn_tense(verb), prep))
            questions.add(u"{} {} {}{} {}?".format(aux, topic, qn_tense(verb), prep, entity))
        else:
            questions.add(u"{} {} {}{} {}?".format(aux, entity, qn_tense(verb), prep, topic))

    return list(questions)


"""The men become friends as they work together, and after his brother abdicates the throne,
the new King relies on Logue to help him make his first wartime radio broadcast
on Britain's declaration of war on Germany in 1939."""
# this is really bad. cf "make" in the above sentence.
# really need some way to get the actual subject/object of the verb
# especially important to at least get the proper subject
# since the NE coincides with the proper object a lot more often
# than the topic coincides with the proper subject
def where_questions(result, n, topic):
    sentence = result['sentences'][n]
    tree = tparse(sentence['parsetree'])
    entities = nent.get_entities(sentence['text'])
    possibilities = []
    # it is also conceivable to want "ORGANIZATION", but way too much work to
    # distinguish that from "who", for instance
    want = [u'LOCATION']
    topic_lower = topic.lower()

    for w in want:
        if w in entities:
            for tmp in entities[w]:
                e = replace_corefs(tmp, result, n)
                if e.lower() in topic_lower:
                    continue
                # found good NE
                verb, prep, tense, obj = locate_verb(e.split(' '), tree)
                if verb != None:
                    possibilities.append((e, verb, prep, tense, obj))

    questions = set()
    for entity, verb, prep, tense, obj in possibilities:
        if tense == 'VBD': # past tense
            aux = 'Did'
        else:
            aux = 'Does'
        if obj:
            questions.add(u"Where {} {} {}{}?".format(aux.lower(), topic, qn_tense(verb), prep))
            # maybe we should add "at" somewhere for this one
            questions.add(u"{} {} {}{} {}?".format(aux, topic, qn_tense(verb), prep, entity))
        else:
            questions.add(u"{} {} {}{} {}?".format(aux, entity, qn_tense(verb), prep, topic))

    return list(questions)


def when_questions(result, n, topic):
    sentence = result['sentences'][n]
    tree = tparse(sentence['parsetree'])
    entities = nent.get_entities(sentence['text'])
    possibilities = []
    want = [u'TIME', u'DATE']
    # print "topic:", topic
    topic_lower = topic.lower()

    for w in want:
        if w in entities:
            for tmp in entities[w]:
                e = replace_corefs(tmp, result, n)
                if e.lower() in topic_lower:
                    continue
                # found good NE
                verb, prep, tense, obj = locate_verb(e.split(' '), tree)
                if verb != None:
                    possibilities.append((e, verb, prep, tense, obj))

    questions = set()
    for entity, verb, prep, tense, obj in possibilities:
        if tense == 'VBD': # past tense
            aux = 'Did'
        else:
            aux = 'Does'
        if obj:
            questions.add(u"When {} {} {}{}?".format(aux.lower(), topic, qn_tense(verb), prep))
            # maybe we should add "at" somewhere for this one
            questions.add(u"{} {} {}{} {}?".format(aux, topic, qn_tense(verb), prep, entity))
        else:
            questions.add(u"{} {} {}{} {}?".format(aux, entity, qn_tense(verb), prep, topic))

    return list(questions)


# the other types of questions seem intractable with just simplistic NER techniques
generate_temp = {'when': when_questions, 'where': where_questions, 'who': who_questions}
generate = defaultdict(lambda: other_questions)
for t in generate_temp:
    generate[t] = generate_temp[t]

def make_questions(text, topic):
    questions = []
    # clf = joblib.load("../data/qntype.joblib.pkl")
    result = loads(core.parse(text))
    for i in xrange(len(result['sentences'])):
        # print result['sentences'][i]['text']
        # classes = clf.predict([result['sentences'][i]['text']])
        classes = ['when', 'where', 'who']
        # print classes
        # print ""
        for c in classes:
            # print c
            questions.extend(generate[c](result, i, topic))
    return questions

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
# def main():
#     if len(sys.argv) != 3:
#         print "usage: ./generateqn.py <article>.txt nquestions"
#         # yes, yes, it just disregards nquestions anyway
#         sys.exit(1)

#     make_generic_qns(sys.argv[1])

def main():
    # ignoring nquestions for now
    # with codecs.open(args.article, 'r', 'utf-8') as f:
    with open(args.article) as f:
        topic = f.readline().rstrip()
        text = f.read()
        print '\n'.join(make_questions(text, topic)[:args.nquestions]) # TODO: actually rank them properly and stuff

    

if __name__ == '__main__':
    main()
