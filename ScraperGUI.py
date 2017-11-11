'''
Created on 15. okt. 2017

@author: einaragust
'''

import tkinter as tk
from urllib import request
from Eparser import Eparser

class ScraperGUI(tk.Frame, Eparser):
    '''
    classdocs
    '''
    def __init__(self, master = None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.parser = Eparser()
        self.createWidgets()
    
    def createListboxForWebsiteScrap(self):
        ##   FRAME FOR LISTBOX  / ( ROW = 1 )   ###
        self.listboxFrame = tk.Frame(self)
        self.listboxFrame.pack(fill = tk.X, anchor = tk.W)
        ###########################################
        
        ###   FOR TAGFRAME AND TAG-LISTBOX   ###
        self.tagFrame = tk.LabelFrame(self.listboxFrame, text = "Tags")
        self.tagFrame.pack(side = tk.LEFT, padx = 5, pady = 5)
        self.tagScrollbar = tk.Scrollbar(self.tagFrame)
        self.tagScrollbar.pack(side = tk.RIGHT, fill = tk.Y)
        self.tagListbox = tk.Listbox(self.listboxFrame, selectmode = tk.SINGLE, \
                                     yscrollcommand = self.tagScrollbar.set)
        self.tagListbox.pack(in_ = self.tagFrame, padx = 5, pady = 5)
        self.tagListbox.bind("<<ListboxSelect>>", self.updateTagSelected)
        self.tagScrollbar.config(command = self.tagListbox.yview)
        ########################################
        
        ###   FOR ATTRIBUTE FRAME AND ATTRIBUTE-LISTBOX   ###
        self.attrFrame = tk.LabelFrame(self.listboxFrame, text = "Attributes")
        self.attrFrame.pack(side = tk.LEFT, padx = 5, pady = 5)
        self.attrScrollbar = tk.Scrollbar(self.attrFrame)
        self.attrScrollbar.pack(side = tk.RIGHT, fill = tk.Y)
        self.attrListbox = tk.Listbox(self.listboxFrame, selectmode = tk.SINGLE, \
                                      yscrollcommand = self.attrScrollbar.set)
        self.attrListbox.pack(in_ = self.attrFrame, padx = 5, pady = 5)
        self.attrListbox.bind("<<ListboxSelect>>", self.updateAttrSelected)
        self.attrScrollbar.config(command = self.attrListbox.yview)
        ###############################################
        
        ###   FOR VALUE FRAME AND VALUE-LISTBOX
        self.valueFrame = tk.LabelFrame(self.listboxFrame, text = "Values")
        self.valueFrame.pack(side = tk.LEFT, padx = 5, pady = 5)
        self.valueScrollbar = tk.Scrollbar(self.valueFrame)
        self.valueScrollbar.pack(side = tk.RIGHT, fill = tk.Y)
        self.valueListbox = tk.Listbox(self.valueFrame, yscrollcommand = self.valueScrollbar.set)
        self.valueListbox.config(width = 30)
        self.valueListbox.pack(in_ = self.valueFrame, padx = 5, pady = 5)
        self.valueScrollbar.config(command = self.valueListbox.yview)
        ###############################################
    
    def createWidgets(self):
        ##   FRAME FOR WEBSITE INPUT / ( ROW = 0 )  ###
        self.websiteScraperFrame = tk.Frame(self)
        self.websiteScraperFrame.pack(fill = tk.BOTH, expand = True, padx = 5, pady = 5)
        ###############################################
        
        ###   FOR LABELFRAME, URL-INPUT, SCRAPER BUTTON AND TRAVERSED LABEL   ###
        self.websiteFrame = tk.LabelFrame(self.websiteScraperFrame)
        self.websiteFrame.pack(fill = tk.BOTH, expand = True, padx = 5, pady = 5)
        self.websiteLabel = tk.Label(self.websiteFrame, text = "Website:")
        self.websiteLabel.pack(side = tk.LEFT, padx = 1, pady = 1)
        
        self.website = tk.StringVar()
        self.website.set("http://")
        self.websiteEntry = tk.Entry(self.websiteFrame, width = 68, textvariable = self.website)
        self.websiteEntry.pack(side = tk.LEFT, padx = 4, pady = 4, \
                                anchor = tk.CENTER)

        self.scrapeBtn = tk.Button(self.websiteFrame, text="GO", command=self.fnGObtn)
        self.scrapeBtn.pack(side = tk.LEFT, padx = 4, pady = 4)
        
        self.htmlOrJson = tk.IntVar()
        self.htmlOrJson.set(1)
        self.htmlRadiobtn = tk.Radiobutton(self.websiteFrame, text = "HTML", variable = self.htmlOrJson, \
                                           value = 1)
        self.htmlRadiobtn.pack(side = tk.LEFT, padx = 4, pady = 4)
        self.jsonRadiobtn = tk.Radiobutton(self.websiteFrame, text = "JSON", variable = self.htmlOrJson, \
                                           value = 2)
        self.jsonRadiobtn.pack(side = tk.LEFT, padx = 4, pady = 4)
        
        self.traversedHTML = tk.StringVar()
        self.traversedHTML.set("")
        self.traversedLabel = tk.Label(self.websiteScraperFrame, textvariable = self.traversedHTML)
        self.traversedLabel.pack(side = tk.BOTTOM, padx = 4, pady = 4) 
        ###############################################
        
        self.createListboxForWebsiteScrap()
        
        
        ###   CREATE FRAME FOR OPTIONS AND OTHER USEFUL STUFF   ###
        self.optionsFrame = tk.Frame(self)
        self.optionsFrame.pack(fill = tk.X, expand = True, padx = 8, pady = 8)

        self.scrapeBtn = tk.Button(self.optionsFrame, text="Export", command=self.exportToFile)
        self.scrapeBtn.pack(side = tk.RIGHT, padx = 4, pady = 4)
        
        self.fileName = tk.StringVar()
        self.fileName.set("")
        self.fileNameEntry = tk.Entry(self.optionsFrame, width = 40, textvariable = self.fileName)
        self.fileNameEntry.pack(side = tk.RIGHT, padx = 4, pady = 4)
        ###############################################
        self.quitBtn = tk.Button(self, text="quit", command= self.quit )
        self.quitBtn.pack(side = tk.RIGHT, padx = 10, pady = 5)
        
        self.destroyBtn = tk.Button(self, text="destroy", command = self.destroyWebsiteScrape)
        self.destroyBtn.pack(side = tk.RIGHT, pady = 5)
        
    def destroyWebsiteScrape(self):
        self.listboxFrame.destroy()
        
        
    def fnGObtn(self):
        # VALIDATE-A URL, !GEYMA URL!
        if self.validateUrl():
            getResponse = request.urlopen(self.website.get())
            print(getResponse.getheaders())
            requestBytes = getResponse.read()
            requestString = requestBytes.decode("utf-8")
            self.parser.feed(requestString)
            getResponse.close()
            for t in self.parser.htmlDoc.keys():
                self.tagListbox.insert(tk.END, t)
            # STILLA AFTUR ENTRY A "http://"
        else:
            print("THIS IS NOT CORRECT URL")

    def validateUrl(self):
        if self.website.get()[0:7] != "http://":
            return False
        else:
            return True
    def exportToFile(self):
        if len(self.fileName.get()) == 0:
            return
        try:
            file = open(self.fileName.get(), 'a')
            for tag in self.parser.htmlDoc:
                file.write(tag + "\n")
                for attr in self.parser.htmlDoc[tag]:
                    file.write("." + attr + "\n")
                    for val in self.parser.htmlDoc[tag][attr]:
                        file.write(".." + val + "\n")
            file.close()
            self.fileName.set("")
        except:
            print("FAT ERROR")
            pass
            
    def updateTagSelected(self, e):
        if self.valueListbox.size() > 0:
            self.valueListbox.delete(0, self.valueListbox.size())
        ## FOR TRAVERSED LABEL ##
        self.traversedArray = []
        self.traversedArray.append(self.tagListbox.get(self.tagListbox.curselection()[0]))
        self.traversedHTML.set(self.traversedArray[0])
        ## END OF TRAV.LABEL ##
        self.attrListbox.delete(0, self.attrListbox.size())
        for a in self.parser.htmlDoc[self.traversedArray[0]].keys():
            self.attrListbox.insert(tk.END, a)
    
    def updateAttrSelected(self, e):
        if self.valueListbox.size() > 0:
            self.valueListbox.delete(0, self.valueListbox.size())
        currAttr = self.attrListbox.get(self.attrListbox.curselection()[0])
        if len(self.traversedArray) > 1:
            self.traversedArray[1] = currAttr
        else:
            self.traversedArray.append(currAttr)
        selectedTag = self.traversedArray[0] + " > " + self.traversedArray[1]
        self.traversedHTML.set(selectedTag)        

        print("TRAVERSED:", self.traversedHTML.get())
        
        for v in self.parser.htmlDoc[self.traversedArray[0]][self.traversedArray[1]]:
            self.valueListbox.insert(tk.END, v)
        
        
if __name__ == "__main__":
    app = ScraperGUI()
    app.master.title("ScraperGUI - v0.1")
    app.master.resizable(width = False, height = False)
    app.mainloop()
