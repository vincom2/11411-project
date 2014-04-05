import codecs

def import_files(filenames):
    documents = {'who': [], 'what': [], 'when': [], 'where': [], 'how': [], 'why': [], 'yn': []}
    for filename in filenames:
        with codecs.open(filename, 'r', 'utf-8') as f:
            temp = []
            for line in f:
                if line[0:2] != u'**':
                    temp.append(line)
                else:
                    documents[line[2:-3].lower()].append(temp[-1])
    return documents
