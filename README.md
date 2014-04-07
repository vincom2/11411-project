NLP final project
=================

Final project for 11-411 NLP. Should consist of 2 components:
* an "asking" program that, given an article and a number n, generates n questions about the article
* an "answering" programing that, given an article and a list of questions, gives answers to the questions.<br/><br/>
N.B. This is a modified incomplete version of the readme for the TAs' reference.

How to use
-----------
* everything necessary should be installed already. Please contact Vincent Huang <vincenth@andrew.cmu.edu> if you encounter problems with missing libraries/requirements.
* In theory, you should be able to use the shell script `ask` with the parameters stated in the project syllabus. Unfortunately, the asker depends on 2 Java programs running as servers, and these 2 programs are memory hogs that sometimes don't like to start properly on unix.andrew, so it would be better if you started them manually and ensured they're actually running. Apologies for the inconvenience. Follow these steps:
  - `source /afs/andrew.cmu.edu/usr14/vincenth/public/11411/11411-project/setenv` (this will modify your path to use python 2.7, and then source my virtualenv scripts.
  - `workon nlpp` (this activates my virtualenv)
  - start a `screen` session, and inside it run `./invoke_corenlp`. Make sure coreNLP actually finishes loading and says it's serving on port 40001 (you can change this to anything you like if you want) before detaching with Ctrl+A D (this is a painful step because coreNLP is really resource-hungry and sometimes just won't load. If that happens, try switching which unix.andrew machine you use. Sorry!)
  - start another `screen` session, and inside it run `./invoke_ner`. This one should be less problematic, but again make sure it runs properly. The default port is 40002; again, feel free to change this.
  - to run the _asker_, `python ask_files/generateqn.py --corenlp-port 40001 --ner-port 40002 <article> <nquestions>`
  - now you can kill the 2 screen sessions since the answerer doesn't use them.
  - to run the _answerer_, `python answer_files/answer.py <article> <questions>`