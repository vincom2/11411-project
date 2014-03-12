NLP final project
=================

Final project for 11-411 NLP. Should consist of 2 components:
* an "asking" program that, given an article and a number n, generates n questions about the article
* an "answering" programing that, given an article and a list of questions, gives answers to the questions.

Repository contents
-------------------
### General organization
Thus far, the repository is organized as follows:
* data/: contains the articles provided as part of the project. also contains extra articles used to train the classifier, and the classifier itself.
* util/: contains utility scripts, e.g.
  - `tokenize.py` to tokenize text
  - `html2text.py` to download Wikipedia articles.
* ask/: contains files that will hopefully be useful for the "asking" component. e.g.
  - `generic.py` contains "generic questions" that can be asked about _any_ article that falls into the categories.
  - `train_classifier.py` trains a naive Bayesian classifier and pickles it
  - `classify.py` loads up a classifier and uses it to classify articles
  - `generateqn.py` is a total skeleton for generating questions :(<br/>
     Right now it can throw out the generic questions in `generic.py`, but that's it.