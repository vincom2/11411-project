#!/usr/bin/python
# the funny thing is I'm adding the #! lines in but I dunno how they interact with
# virtualenvs, so I run the scripts with python script.py anyway... :P

# see http://stackoverflow.com/questions/10098533/implementing-bag-of-words-naive-bayes-classifier-in-nltk
# hopefully that is useful D:
# current code is mostly adapted from http://streamhacker.com/2010/05/10/text-classification-sentiment-analysis-naive-bayes-classifier/

# very bad code with paths hardcoded everywhere :o

import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus.reader import CategorizedPlaintextCorpusReader
import pickle

corpusdir = '../data/own'

def word_feats(words):
    return dict([(word, True) for word in words])

def hold_back(len):
    if len <= 4:
        return 1
    else:
        return len/4

def main():
    articles = CategorizedPlaintextCorpusReader(corpusdir, '.*', cat_pattern = r'(.*)[/]')
    feats = {}
    trainfeats = []
    testfeats = []
    for cat in articles.categories():
        wow = len([f for f in articles.fileids(cat)]) # such variable name
        print "for category", cat, ":", wow
        feats[cat] = [(word_feats(articles.words(fileids = [f])), cat) for f in articles.fileids(cat)]
        cutoff = wow - hold_back(wow)
        trainfeats.append(feats[cat][:cutoff])
        testfeats.append(feats[cat][cutoff:])

    train = [item for sublist in trainfeats for item in sublist]
    test = [item for sublist in testfeats for item in sublist]

    print 'train on %d instances, test on %d instances' % (len(train), len(test))

    classifier = NaiveBayesClassifier.train(train)
    print 'accuracy:', nltk.classify.util.accuracy(classifier, test)
    classifier.show_most_informative_features() # I don't understand the output for more than 2 categories :(

    # load with:
    # import pickle
    # f = open('my_classifier.pickle')
    # classifier = pickle.load(f)
    # f.close()
    with open('../data/classifier.pickle', 'wb') as f:
        pickle.dump(classifier, f)
        # wtf it's 50MB
        # use cPickle or import gzip or import bz2 or something
