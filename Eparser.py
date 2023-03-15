from html.parser import HTMLParser
from queue import LifoQueue
        
class ProperyData:
    def __init__(self, prop, data = None):
        self.attrs = prop
        self.data = data
   
    def getAttribute(self):
        if len(self.attrs[0]) > 0:
            return self.attrs[0][0]
    
    def getProperty(self):
        return self.attrs[0][1]
    
class Eparser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.htmlDoc = {}
        self.tags = LifoQueue(0)
        self.currentData = None

    def handle_starttag(self, tag, attrs):
        self.tags.put({'tag': tag, 'attrs': attrs})
            
    def handle_endtag(self, tag):
        if tag not in self.htmlDoc:
            self.htmlDoc[tag] = {}
        obj = self.tags.get()
        if self.currentData:
            if obj['attrs']:
                if obj['attrs'][0][0] not in self.htmlDoc[tag]:
                    self.htmlDoc[tag][obj['attrs'][0][0]] = []
                self.htmlDoc[tag][obj['attrs'][0][0]].append({'prop': obj['attrs'][0][1], 'data': self.currentData})
        self.currentData = None
       
    def handle_data(self, data):
        cleanString = data.rstrip("\t \n")
        if len(cleanString) > 3:
            self.currentData = cleanString