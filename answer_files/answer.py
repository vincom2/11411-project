#!/usr/bin/env python

"""TODO:
   identify if question is a yes/no question. if it's a yn question, after extracting the most relevant sentence,
   check if it's negative. If it is, say no. Otherwise, say yes. We probably want to be a lot more careful about this,
   but this will do for a start."""

from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords as stopwords_
import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument("article", help="the article to get answers from")
parser.add_argument("questions", help="the text file containing questions, one per line")

punkt_param = PunktParameters()
punkt_param.abbrev_types = set(['dr', 'vs', 'mr', 'mrs', 'prof', 'inc', 'v'])
sentence_splitter = PunktSentenceTokenizer(punkt_param)

yn_words = ['Did', 'Does', 'Do', 'Has', 'Have', 'Had', 'Was', 'Is', 'Are', 'Were'] # are there more? there probably are
yn_regex = re.compile(r'^({})'.format('|'.join(yn_words)))

neg_regex = re.compile(r"(.*\b(?:{})\b)|(.*n't)".format('|'.join(['not','no'])))

def find_max(values):
    max, maxi = 0, 0
    for i in xrange(len(values)-1):
        if values[i] > max:
            max, maxi = values[i], i

    return maxi

def yn_question(question):
    if yn_regex.match(question):
        return True
    else:
        return False

def neg_answer(answer):
    if neg_regex.match(answer):
        return True
    else:
        return False

def read_article(filename):
    with open(filename) as f:
        text = f.read()
    return sentence_splitter.tokenize(text, realign_boundaries=True)

def main():
    args = parser.parse_args()
    sentences = read_article(args.article)
    stopwords = stopwords_.words('english')
    # maybe don't use stopwords? they should have low scores anyway
    # maybe do named entity replacement first?
    vect = TfidfVectorizer(min_df=1, stop_words=stopwords)

    with open(args.questions) as f:
        for qn in f:
            documents = sentences + [qn]
            matrix = vect.fit_transform(documents)
            values = cosine_similarity(matrix[-1:], matrix)
            # print "Q:", qn
            # print "A:", sentences[find_max(values[0])]
            tmp = sentences[find_max(values[0])].split('\n')[-1]
            if not yn_question(qn):
                print tmp
            elif neg_answer(tmp):
                print "Nope."
            else:
                print "Yes."


if __name__ == '__main__':
    main()
