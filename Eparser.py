from html.parser import HTMLParser

class Eparser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.htmlDoc = {}
        self.tags = []
        
    def handle_starttag(self, tag, attrs):
        self.tags.append(tag)
        if tag not in self.htmlDoc:
            self.htmlDoc[tag] = {}
        for attr in attrs:
            try:
                if attr[0] not in self.htmlDoc[tag]:
                    self.htmlDoc[tag][attr[0]] = []
                self.htmlDoc[tag][attr[0]].append(attr[1])
            except:
                self.htmlDoc[tag][attr[0]].append("ATTRIBUTE CORRUPTED")
                pass
            
    def handle_endtag(self, tag):
        self.tags.pop()
        
    def handle_data(self, data):
        cleanString = data.rstrip("\t")
        if len(cleanString) > 3 and len(self.tags) > 0:
            try:
                if "DATA" not in self.htmlDoc[self.tags[len(self.tags)-1]]:
                    self.htmlDoc[self.tags[len(self.tags)-1]]["DATA"] = []
                self.htmlDoc[self.tags[len(self.tags)-1]]["DATA"].append(data)
            except:
                self.htmlDoc[self.tags[len(self.tags)-1]]["DATA"].append("DATA CORRUPTED")
                pass