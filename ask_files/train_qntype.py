#!/usr/bin/env python

# for importing data
import sys, os, glob
sys.path.append(os.path.abspath('../util'))
from import_data import import_files
from collections import defaultdict
# scikit-learn stuff
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.multiclass import OneVsRestClassifier
from sklearn.cross_validation import train_test_split
from sklearn.externals import joblib

filenames = glob.iglob("../util/*.out")
outfile = '../data/qntype.joblib.pkl'
categories = {'who': 0, 'what': 1, 'when': 2, 'where': 3, 'why': 4, 'how': 5}
target_names = [None] * 6
for cat in categories:
    target_names[categories[cat]] = cat


def save_classifier(classifier, outfile):
    joblib.dump(classifier, outfile, compress=9)

def main():
    data = import_files(filenames)
    sentences = defaultdict(lambda: [])
    # invert the dictionary
    for cat in data:
        if cat == 'yn':
            continue
        for sentence in data[cat]:
            sentences[sentence].append(cat)

    X_list = []
    y_data = []
    for s in sentences:
        X_list.append(s)
        y_data.append(sentences[s])
    X_data = np.array(X_list)

    # X_train, X_test, y_train, y_test = train_test_split(X_data, y_data, test_size=0.01, random_state=802701)\
    X_train = X_data
    y_train = y_data

    classifier = Pipeline([
                    ('vectorizer', TfidfVectorizer()),
                    ('clf', OneVsRestClassifier(LinearSVC()))])
    classifier.fit(X_train, y_train)

    save_classifier(classifier, outfile)

    # predicted = classifier.predict(X_test)
    # return (y_test, predicted)

    # for item, labels, actuals in zip(X_test, predicted, y_test):
    #     print item, '=>', ', '.join(target_names[i] for i in labels)
    #     print "actual labels are:", ', '.join(target_names[i] for i in actuals)

if __name__ == '__main__':
    main()
