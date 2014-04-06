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
  - `tag_qn_type.py` to tag article sentences with the types of questions that could be generated from them. Read the instructions!
* ask/: contains files that will hopefully be useful for the "asking" component. e.g.
  - `generic.py` contains "generic questions" that can be asked about _any_ article that falls into the categories.
  - `train_classifier.py` trains a naive Bayesian classifier and pickles it. This classifier classifies articles into one of the 5 classes of provided articles (so it's probably not going to be very useful).
  - `classify.py` loads up a classifier and uses it to classify articles (see the comments for `train_classifier.py`)
  - `generateqn.py` now sort of generates "who questions" (great emphasis on "sort of", because _the questions are *terrible*_)
  - `SumBasic.py` summarises stuff. It's probably not useful and can be disregarded.
  - `train_qntype.py` trains a classifier that classifies sentences into what kinds of questions they can be turned into (who, what, when, where, how, why). The classifier's currently at `data/qntype.joblib.pkl`.
* corenlp/: contains python wrappers for Stanford CoreNLP.
  - You need to install CoreNLP separately. Get version 3.3.1 at http://nlp.stanford.edu/software/stanford-corenlp-full-2014-01-04.zip and make sure your JRE is sufficiently recent. Follow instructions at https://bitbucket.org/torotoki/corenlp-python.
  - You also need to install Stanford NER, since the pyner wrapper uses it (I know it seems silly since NER is included in CoreNLP, but pyner provides output that's a lot nicer to use...). Get version 3.3.1 at http://nlp.stanford.edu/software/stanford-ner-2014-01-04.zip and make sure your JRE is sufficiently recent. Follow instructions at https://github.com/dat/pyner (although you should `pip install ner` instead)

How to use
-----------
Yes, it now generates (really bad) questions! To use:
* install the stuff the readme says to install above, and also the stuff in `requirements.txt`.
* You could use `ask_script` if you have the exact same setup as me, including using virtualenvwrapper with a virtualenv named nlpp and stuff. I must confess that I wasn't thinking about deploying to other systems when I started, so we'll have to figure this out >.>
* Otherwise, if the script doesn't work for you, well, run the commands in it manually. It'll generate questions! Yay! (right now it ignores nquestions)