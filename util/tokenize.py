#!/usr/bin/env python
"""incredibly poor "tokenizer". All it does is break everything up and put it into one line.
   Since things like headings will probably be useful, even in plaintext, since they indicate the kinds of questions
   that might be generated from that section, we should probably make it at least treat those more "properly"
   eventually."""

import nltk
import sys

def main():
    if len(sys.argv) != 3:
        print "Usage: ./tokenize.py <input> <output>"
        sys.exit(1)

    with open(sys.argv[1]) as input:
        data = input.read()

    tok = nltk.word_tokenize(data)

    with open(sys.argv[2],'w') as output:
        output.write(' '.join(tok))

if __name__ == '__main__':
    main()
