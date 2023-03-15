import tkinter as ttk
import tkinter.filedialog as openFile

from urllib import request
from Eparser import Eparser

class Manager(object):
    def __init__(self, gui):
       self.isWebsite = False
       self.parser = Eparser()
       self.gui = gui
       self.gui.listbox_frame.manager = self
       self.gui.input_frame.manager = self
       self.gui.headers_frame.manager = self
    
    def btnScrape(self, filename):
        if len(filename) < 5:
            print("Not a file or a url!")
        else:
            if filename[0:4] == ("http"):
                getResponse = request.urlopen(filename)
                print(getResponse.getheaders())
                requestBytes = getResponse.read()
                requestString = requestBytes.decode("utf-8")
                self.parser.feed(requestString)
                getResponse.close()
                self.__create_widgets(getResponse.getheaders())
                
            else:
                f = open(filename, 'r', encoding='utf-8')
                requestBytes = f.read()
                self.parser.feed(requestBytes)
                f.close()
            for t in self.parser.htmlDoc.keys():
                self.gui.listbox_frame.tagListbox.insert(ttk.END, t)

    def __create_widgets(self, headers):
        r = 0
        for h in headers:
            column = 0
            ttk.Label(self.gui.headers_frame, text=h[0]).grid(row=r, column=column)
            column += 1
            ttk.Label(self.gui.headers_frame, text=h[1]).grid(row=r, column=column)
            r += 1

class HeadersFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.manager = None

class InputFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.__create_widgets()
        self.manager = None
    
    def __create_widgets(self):
        self.urlFile = ttk.Label(self, text = "Url / File:").grid(column=0, row=0, sticky=ttk.W)
        self.urlFileName = ttk.StringVar()
        self.urlFileEntry = ttk.Entry(self, width=100, textvariable = self.urlFileName)
        self.urlFileEntry.focus()
        self.urlFileEntry.grid(column=1, row=0, sticky=ttk.W)
        ttk.Button(self, text="Scrape", command=self.btnScrape, underline=0, takefocus=True).grid(column=2, row=0, ipadx=3, sticky="NEWS")
        ttk.Button(self, text="Open file..", command=self.btnOpenFile, underline=0, takefocus=True).grid(column=3, row=0, ipadx=3, sticky="NEWS")
        for widget in self.winfo_children():
            widget.grid(padx=5, pady=5)

    def btnScrape(self):
        self.manager.btnScrape(self.urlFileName.get())

    def btnOpenFile(self):
        filename = openFile.askopenfilename(initialdir="/", title="Select file", filetypes=[('HTML', '*.html')])
        self.urlFileName.set(filename)

class ListboxFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.theWay = ttk.StringVar()

        self.__create_widgets()
        self.manager = None
        self.selected = { 'tag': None, 'attr': None, 'prop': None }
    
    def __create_widgets(self):
        # TAG SCROLL AND LISTBOX #
        ttk.Label(self, text = "Tags").grid(row=0, column=0, sticky=ttk.S+ttk.E+ttk.W+ttk.N)

        tagScrollbar = ttk.Scrollbar(self, orient=ttk.VERTICAL)
        tagScrollbar.grid(row=1, column=1, rowspan=8, sticky=ttk.N+ttk.S)

        self.tagListbox = ttk.Listbox(self, yscrollcommand=tagScrollbar.set, selectmode=ttk.SINGLE, exportselection=False)
        self.tagListbox.grid(row=1, column=0, rowspan=8,  padx=(5,0), sticky=ttk.S+ttk.E+ttk.W+ttk.N)

        self.tagListbox.bind("<<ListboxSelect>>", self.updateAttrListbox)
        tagScrollbar['command'] = self.tagListbox.yview

        # ATTR SCROLL AND LISTBOX
        ttk.Label(self, text = "Attributes").grid(row=0, column=2, sticky=ttk.S+ttk.E+ttk.W+ttk.N)
        attrScrollbar = ttk.Scrollbar(self, orient=ttk.VERTICAL)
        attrScrollbar.grid(row=1, column=3, rowspan=8,  padx=0, sticky=ttk.N+ttk.S)

        self.attrListbox = ttk.Listbox(self, yscrollcommand=attrScrollbar.set, selectmode=ttk.SINGLE, exportselection=False)
        self.attrListbox.grid(row=1, column=2, rowspan=8,  padx=(10,0), sticky=ttk.S+ttk.E+ttk.W+ttk.N)
        
        self.attrListbox.bind("<<ListboxSelect>>", self.updateValueListbox)
        attrScrollbar['command'] = self.attrListbox.yview

        # PROPERY SCROLL AND LISTBOX
        self.columnconfigure(4, weight=2)
        ttk.Label(self, text="Value").grid(row=0, column=4, sticky=ttk.S+ttk.E+ttk.W+ttk.N)
        valueScrollbar = ttk.Scrollbar(self, orient=ttk.VERTICAL)
        valueScrollbar.grid(row=1, column=5, rowspan=8,  sticky=ttk.N+ttk.S)
        self.valueListbox = ttk.Listbox(self, yscrollcommand=valueScrollbar.set, selectmode=ttk.SINGLE, exportselection=False)
        self.valueListbox.grid(row=1, column=4, rowspan=8,  padx=(5,0), sticky=ttk.S+ttk.E+ttk.W+ttk.N)
        valueScrollbar['command'] = self.valueListbox.yview
        self.valueListbox.bind("<<ListboxSelect>>", self.updateTheData)
        # LABEL FOR DATA AND SELECTED TAG, ATTRIBUTE & (PROPERTY)
        self.theData = ttk.StringVar()
        self.columnconfigure(6, weight=1)
        self.columnconfigure(7, weight=1)
        ttk.Label(self, text="Traveling: ").grid(row=10, column=0, sticky=ttk.E+ttk.W+ttk.N)
        ttk.Label(self, textvariable=self.theWay).grid(row=10, column=1, columnspan=5, sticky=ttk.E+ttk.W+ttk.N)
        ttk.Label(self, text="DATA:").grid(row=11, column=0, sticky=ttk.E+ttk.W+ttk.N)
        self.currentData = ttk.Label(self, textvariable=self.theData).grid(row=11, column=1, columnspan=4, sticky=ttk.W+ttk.N)
        
    def updateTheData(self, e):
        currProp = self.valueListbox.get(self.valueListbox.curselection())
        data = self.manager.parser.htmlDoc[self.selected['tag']][self.selected['attr']][currProp][0]
        self.theWay.set(f'{self.selected["tag"]} > {self.selected["attr"]} > {currProp}')
        if (len(data) > 30):
            self.theData.set(data[0:30])
        else:
            self.theData.set(data)
        
    def updateAttrListbox(self, e):
        if self.valueListbox.size() > 0:
            self.valueListbox.delete(0, self.valueListbox.size())
            self.theData.set("")
            self.theWay.set("")
        self.selected['tag'] = self.tagListbox.get(self.tagListbox.curselection())
        self.theWay.set(self.selected['tag'])
        if self.attrListbox.size() > 0:
            self.attrListbox.delete(0, self.attrListbox.size())
        for a in self.manager.parser.htmlDoc[self.selected['tag']].keys():
            self.attrListbox.insert(ttk.END, a)

    def updateValueListbox(self, e):
        currSelectet = self.attrListbox.curselection()
        if currSelectet != ():
            self.selected['attr'] = self.attrListbox.get(self.attrListbox.curselection())
            self.theWay.set(f'{self.selected["tag"]} > {self.selected["attr"]}')
            self.valueListbox.delete(0, self.valueListbox.size())
            for a in self.manager.parser.htmlDoc[self.selected['tag']][self.selected['attr']].keys():
                self.valueListbox.insert(ttk.END, a)


class OptionsFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.__create_widgets()
        self.manager = None
    
    def __create_widgets(self):
        self.tags = ttk.StringVar()
        self.attrs = ttk.StringVar()
        self.classname = ttk.StringVar()
        self.tag_id = ttk.StringVar()

        fetchLabelFrame = ttk.LabelFrame(self, text="Fetch only?", borderwidth=2)
        fetchLabelFrame.grid(row=0, column=0, columnspan=3, pady=10, padx=10, ipadx=5, ipady=5, sticky="NEWS")
        ttk.Label(fetchLabelFrame, text="Tags:").grid(row=1, column=0, pady=(5,0), sticky="WNE")
        ttk.Entry(fetchLabelFrame, width=50, textvariable=self.tags).grid(row=1, column=1, pady=(5,0), sticky="NEWS")
        ttk.Label(fetchLabelFrame, text="Attributes:").grid(row=2, column=0, pady=(5,0), sticky="WNE")
        ttk.Entry(fetchLabelFrame, width=50, textvariable=self.attrs).grid(row=2, column=1, pady=(5,0), sticky="NEWS")

        showDataInLabelFrame = ttk.LabelFrame(self, text="Show data inside:", borderwidth=2)
        showDataInLabelFrame.grid(row=3, column=0, columnspan=3, pady=10, padx=10, ipadx=5, ipady=5, sticky="NEWS")
        ttk.Label(showDataInLabelFrame, text="Class:").grid(row=4, column=0, pady=(5,0), sticky="WNE")
        ttk.Entry(showDataInLabelFrame, width=50, textvariable=self.classname).grid(row=4, column=1, pady=(5,0), sticky="NEWS")
        ttk.Label(showDataInLabelFrame, text="id:").grid(row=5, column=0, pady=(5,0), sticky="WNE")
        ttk.Entry(showDataInLabelFrame, width=50, textvariable=self.tag_id).grid(row=5, column=1, pady=(5,0), sticky="NEWS")



class ApplicationGUI(ttk.Tk):
    '''
    classdocs
    '''
    def __init__(self):
        super().__init__()
        self.title("ScraperGUI - v0.1")
        self.resizable(width = False, height = False)
        #self.geometry("700x700")
        self.attributes('-toolwindow', True)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)
        self.__create_widgets()
    
    def __create_widgets(self):
        self.input_frame = InputFrame(self)
        self.input_frame.grid(column=0, row=0, sticky="WENS")

        self.listbox_frame = ListboxFrame(self)
        self.listbox_frame.grid(column=0, row=1, sticky="WENS", pady=(0, 5), padx=5)

        self.headers_frame = HeadersFrame(self)
        self.headers_frame.grid(column=0, row=2, sticky="WENS")

        #self.options_frame = OptionsFrame(self)
        #self.options_frame.grid(column=0, row=1, rowspan=4, columnspan=4, sticky="ENS")




if __name__ == "__main__":
    app = ApplicationGUI()
    Manager(app)
    app.mainloop()