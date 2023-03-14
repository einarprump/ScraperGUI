from html.parser import HTMLParser
import pprint

class Attributes:
    def __init__(self, attrs):
        self.attrs = attrs
        self.data = None
    
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
                self.tmpClass = { 'tag': tag, 'attr': attr[0], 'prop': attr[1] }
                if attr[0] not in self.htmlDoc[tag]:
                    self.htmlDoc[tag][attr[0]] = []
                self.htmlDoc[tag][attr[0]].append(attr[1])
                #if attr[0] == 'src' or (attr[0] == 'href' and attr[1][-4][0] == '.'):
                #    print(attr[0], " : ", attr[1])
            except:
                print('ERROR')
                pass
            
    def handle_endtag(self, tag):

        pass
        
    def handle_data(self, data):
        cleanString = data.rstrip("\t \n")
        if len(cleanString) > 3:
            if self.tmpClass['tag'] != "script" and self.tmpClass['tag'] != "style" and self.tmpClass['tag'] != "meta":
                print(f"WE HAVE DATA!!  -> {cleanString}   : {self.tmpClass['tag']} - {self.tmpClass['attr']} - {self.tmpClass['prop']}")

