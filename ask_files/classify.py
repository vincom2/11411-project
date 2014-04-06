#!/usr/bin/env python

import os.path
import nltk
import pickle
import sys
from train_classifier import word_feats

classifier_loc = "../data/classifier.pickle"

def load_article(article):
    with open(article) as f:
        input = f.read()

    return word_feats(nltk.word_tokenize(input))

def classify(article):
    with open(classifier_loc) as f:
        classifier = pickle.load(f)

    return classifier.classify(load_article(article))


def main():
    if len(sys.argv) != 2:
        print "usage: ./classify.py <classifythis.txt>"
        sys.exit(1)

    # this is horrendously slow and we probably need a good way to ameliorate it
    # classify large batches at a go?
    # or maybe a binary format will load faster
    # INVESTIGATE
    with open(classifier_loc) as f:
        classifier = pickle.load(f)

    with open(sys.argv[1]) as f:
        input = f.read()

    data = word_feats(nltk.word_tokenize(input))

    print classifier.classify(data)

if __name__ == '__main__':
    main()
