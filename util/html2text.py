"""feed this a text file containing one URL per line
   and a directory for it to place its output in.
   It will download the HTML content at the URL, clean it up (however NLTK cleans HTML up),
   and then do some other stuff, and then save it to "outputdir/<url-after-last-slash>.txt".
   As you can see, it was clearly written for wikipedia articles, hence the <url-after-last-slash>
   and the part where it strips out text of the form "[ 20 ]". Lol."""

from nltk.util import clean_html
import urllib2
import re
import sys
import os
import os.path

remove_footnotes = re.compile(r'\[.*\]')

def main():
    if len(sys.argv) != 3:
        print "usage: ./html2text.py <urlfile> <outputdir>"
        sys.exit(1)

    with open(sys.argv[1]) as f:
        urls = [line.rstrip('\n') for line in f]


    for url in urls:
        filename = url.rsplit('/',1)[1] + ".txt"
        response = urllib2.urlopen(url)
        text = clean_html(response.read())
        cleaned_text = re.sub(remove_footnotes, '', text)
        # wow such race condition
        if not os.path.exists(sys.argv[2]):
            os.makedirs(sys.argv[2])
        with open(os.path.join(sys.argv[2], filename), 'w') as f:
            f.write(cleaned_text)

if __name__ == '__main__':
    main()
