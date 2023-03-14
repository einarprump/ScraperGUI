from html.parser import HTMLParser
from queue import LifoQueue

class Attributes:
    def __init__(self, attrs):
        self.attrs = attrs
        self.data = None
    
class Eparser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.htmlDoc = {}
        self.tmpClass = {}
        self.tags = LifoQueue(0)
        self.currentData = None

    def handle_starttag(self, tag, attrs):
        self.tags.put({'tag': tag, 'attrs': attrs})
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
        obj = self.tags.get()
        if self.currentData:
            print('OBJ:', obj, " : ", self.currentData[0:4])

        
    def handle_data(self, data):
        cleanString = data.rstrip("\t \n")
        if len(cleanString) > 3:
            self.currentData = cleanString
            #if self.tmpClass['tag'] != "script" and self.tmpClass['tag'] != "style" and self.tmpClass['tag'] != "meta":
            #    pass
                #print(f"WE HAVE DATA!!  -> {cleanString}   : {self.tmpClass['tag']} - {self.tmpClass['attr']} - {self.tmpClass['prop']}")

