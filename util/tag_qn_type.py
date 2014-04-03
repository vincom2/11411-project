#!/usr/bin/env python

"""TAGGING INSTRUCTIONS
   If you don't know what to tag it with, reject with 'n' or just give the generic 'yn' tag!
   But seriously, 'yn' is a generic tag, since pretty much everything can be a polar question.
   If you have any other tags, please don't put the 'yn' tag. Just use it if you don't want to
   reject a sentence but don't have an alternative tag.
   You can use multiple tags for one sentence! just separate them with spaces on the same line.
   If you see a shitty "sentence", just 'n' it. punkt the tokenizer sucks."""

from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters
import sys

punkt_param = PunktParameters()
punkt_param.abbrev_types = set(['dr', 'vs', 'mr', 'mrs', 'prof', 'inc', 'v'])
sentence_splitter = PunktSentenceTokenizer(punkt_param)

valid_tags = frozenset(['who','what','when','where','how','why','yn'])

def output_tags(f, sentence, tags):
    for tag in tags:
        f.write(sentence + '\n**' + tag.upper() + '**\n\n')

# cool shit stolen from http://stackoverflow.com/questions/14374181/moving-back-an-iteration-in-a-for-loop
def repeatable(it):
    buf, it = None, iter(it)
    while True:
        if buf is None:
            # the buffer is empty, send them the next elem
            val = next(it)
        else:
            # there's something in the buffer
            # let's send that back
            val = buf

        # send the value and wait what they say
        back = yield val

        if back:
            # they've sent us something!
            # give them some dummy value as a result of send()
            yield None 
            # and save what they've sent in a buffer
            # for the next iteration
            buf = back

        else:
            # they haven't sent anything
            # empty the buffer
            buf = None


def main():
    if len(sys.argv) != 3:
        print "usage: tag_qn_type.py infile outfile"
        sys.exit(1)

    print "when presented with a sentence, answer some of (separated by spaces)"
    print "who/what/when/where/how/why/yn to indicate question type"
    print "or n to indicate that you think sentence should not be made into a question"
    print "or quit to terminate early"

    with open(sys.argv[1]) as f:
        text = f.read()

    sentences = sentence_splitter.tokenize(text, realign_boundaries=True)
    sentences_ = repeatable(sentences)
    with open(sys.argv[2], 'w') as f:
        for sentence in sentences_:
            cat = raw_input(sentence + ": ")
            cat = cat.lower()
            if cat == 'quit' or cat == 'exit':
                print "bye!"
                sys.exit(0)
            elif cat == 'n':
                continue
            else:
                tags = cat.split(' ')
                if set(tags) <= valid_tags:
                    output_tags(f, sentence, tags)
                    print ""
                else:
                    print "************************************************************************"
                    print "\t\tINVALID INPUT, PLEASE TRY AGAIN"
                    print "************************************************************************"
                    sentences_.send(sentence)


if __name__ == '__main__':
    main()
