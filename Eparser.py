from html.parser import HTMLParser
import pprint

class Eparser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.htmlDoc = {}
        self.tmpClass = {}

    def display(self):
        pp = pprint.PrettyPrinter(indent=2)
        pp.pprint(self.htmlDoc)

    def handle_starttag(self, tag, attrs):
        if tag not in self.htmlDoc:
            self.htmlDoc[tag] = {}
          
        for attr in attrs:
            try:
                if attr[0] not in self.htmlDoc[tag]:
                    self.htmlDoc[tag][attr[0]] = []
                self.htmlDoc[tag][attr[0]].append(attr[1])
                if attr[0] == 'class':
                    self.tmpClass = { 'tag': tag, 'attr': attr[0]}
            except:
                print('ERROR')
                #self.htmlDoc[tag][attr[0]].append("ATTRIBUTE CORRUPTED")
                pass
            
    def handle_endtag(self, tag):
        pass
        #if tag == 'div' and 'data' in self.d:
        #    if self.tmp != {}:
        #        if 'attrs' in self.tmp:
        #            if len(self.tmp['attrs']) > 0:
        #                self.htmlDoc[tag].append(self.tmp)
        #self.tmpClass = {}
        #self.workingNode = self.htmlDoc.traverseNode()
        
    def handle_data(self, data):
        cleanString = data.rstrip("\t")
        if len(cleanString) > 3 and self.tmpClass:
            self.htmlDoc[self.tmpClass['tag']][self.tmpClass['attr']].append(cleanString)

#if __name__ ==  "__main__":
#    parser = Eparser()
#    f = open(r"C:\Users\einar\Documents\champ-fyrir-11.03\Premier League Live Scores, Results & Fixtures _ LiveScore.html", 'r', encoding='utf-8')
#    requestBytes = f.read()
#    parser.feed(requestBytes)
#    f.close()
#    parser.display()
