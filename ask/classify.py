# see http://stackoverflow.com/questions/10098533/implementing-bag-of-words-naive-bayes-classifier-in-nltk
# hopefully that is useful D:
# current code is mostly adapted from http://streamhacker.com/2010/05/10/text-classification-sentiment-analysis-naive-bayes-classifier/

import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus.reader import CategorizedPlaintextCorpusReader

corpusdir = '../data/organized'
articles = CategorizedPlaintextCorpusReader(corpusdir, '.*', cat_pattern = r'(.*)[/]')

def word_feats(words):
    return dict([(word, True) for word in words])

def hold_back(len):
    if len <= 4:
        return 1
    else:
        return len/4

feats = {}
trainfeats = []
testfeats = []
for cat in articles.categories():
    feats[cat] = [(word_feats(articles.words(fileids = [f])), cat) for f in articles.fileids(cat)]
    cutoff = len(feats[cat]) - hold_back(len(feats[cat]))
    trainfeats.append(feats[cat][:cutoff])
    testfeats.append(feats[cat][cutoff:])

train = [item for sublist in trainfeats for item in sublist]
test = [item for sublist in testfeats for item in sublist]

print 'train on %d instances, test on %d instances' % (len(trainfeats), len(testfeats))

classifier = NaiveBayesClassifier.train(train)
print 'accuracy:', nltk.classify.util.accuracy(classifier, test)
classifier.show_most_informative_features() # I don't understand the output for more than 2 categories :()
