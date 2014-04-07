#!/usr/bin/env python

from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords as stopwords_
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("article", help="the article to get answers from")
parser.add_argument("questions", help="the text file containing questions, one per line")

punkt_param = PunktParameters()
punkt_param.abbrev_types = set(['dr', 'vs', 'mr', 'mrs', 'prof', 'inc', 'v'])
sentence_splitter = PunktSentenceTokenizer(punkt_param)

def find_max(values):
    max, maxi = 0, 0
    for i in xrange(len(values)-1):
        if values[i] > max:
            max, maxi = values[i], i

    return maxi

def read_article(filename):
    with open(filename) as f:
        text = f.read()
    return sentence_splitter.tokenize(text, realign_boundaries=True)

def main():
    args = parser.parse_args()
    sentences = read_article(args.article)
    stopwords = stopwords_.words('english')
    vect = TfidfVectorizer(min_df=1, stop_words=stopwords)

    with open(args.questions) as f:
        for qn in f:
            documents = sentences + [qn]
            matrix = vect.fit_transform(documents)
            values = cosine_similarity(matrix[-1:], matrix)
            print "Q:", qn
            print "A:", sentences[find_max(values[0])]

if __name__ == '__main__':
    main()
