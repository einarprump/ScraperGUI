from html.parser import HTMLParser
from queue import LifoQueue

class AttributesDictList:
    def __init__(self):
        self.attributes = {}
    
    def addAttrData(self, attr):
        if attr[0]:
            if attr[0] not in self.attributes:
                self.attributes[attr[0]] = []
            self.attributes[attr[0]].append(attr)
            
        
class ProperyData:
    def __init__(self, prop, data = None):
        self.attrs = prop
        self.data = data
        #print("TYPE:", type(attrs))
        #print("ATTRS:", attrs)
        #print("DATA:", data)
        if not attrs:
            self.attrs.append(('None', 'None'))
   
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
                #append(Attributes(obj['attrs'], self.currentData))
        self.currentData = None
       
    def handle_data(self, data):
        cleanString = data.rstrip("\t \n")
        if len(cleanString) > 3:
            self.currentData = cleanString
            #if self.tmpClass['tag'] != "script" and self.tmpClass['tag'] != "style" and self.tmpClass['tag'] != "meta":
            #    pass
                #print(f"WE HAVE DATA!!  -> {cleanString}   : {self.tmpClass['tag']} - {self.tmpClass['attr']} - {self.tmpClass['prop']}")

