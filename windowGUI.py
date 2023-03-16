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
                req = request.Request(filename)
                req.add_header('User-Agent', 'HomeMade-Browser/0.1 - In Development')
                getResponse = request.urlopen(req)
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
            ttk.Label(self.gui.headers_frame, text=h[0]).grid(row=r, column=column, sticky="W")
            column += 1
            ttk.Label(self.gui.headers_frame, text=h[1]).grid(row=r, column=column, columnspan=5, sticky="W")
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

class TreeView(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
    
    def initialize(self, data):
        print("INITIALIZING...")
        tree = ttk.Treeview(self)
        tree.heading('#0', text='Scraped', anchor=ttk.W)
        tree.insert('', ttk.END)

class OptionsFrame(ttk.Frame):

    TAGENTRY = "Ex: span,li,..."
    ATTRENTRY = "Ex: rel,alt,..."

    def __init__(self, container):
        super().__init__(container)
        self.__create_widgets()
        self.manager = None
    
    def __create_widgets(self):
        ttk.Label(self, text="Normal scraping behavior is that all tags are harvested,\n to change that check tags and/or attributes to harvest.", anchor="e").grid(row=0, column=0, columnspan=2, sticky="WENS")
        # TAGS TO SCRAPE #
        self.head = ttk.StringVar()
        self.img = ttk.StringVar()
        self.a = ttk.StringVar()
        self.div = ttk.StringVar()
        self.meta = ttk.StringVar()
        
        self.addTag = ttk.StringVar()
        self.addTag.set(self.TAGENTRY)

        tagLabelFrame = ttk.LabelFrame(self, text="Tags", borderwidth=1)
        tagLabelFrame.grid(row=1, column=0, pady=10, padx=10, ipadx=5, ipady=5, sticky="NEWS")
        ttk.Checkbutton(tagLabelFrame, text="head", variable=self.head, onvalue="head", offvalue="").grid(row=0, column=0, pady=(1,0), padx=(5,0), sticky="W")
        ttk.Checkbutton(tagLabelFrame, text="img", variable=self.img, onvalue="img", offvalue="").grid(row=1, column=0, pady=(1,0), padx=(5,0), sticky="W")
        ttk.Checkbutton(tagLabelFrame, text="a", variable=self.a, onvalue="a", offvalue="").grid(row=2, column=0, pady=(1,0), padx=(5,0), sticky="W")
        ttk.Checkbutton(tagLabelFrame, text="div", variable=self.div, onvalue="div", offvalue="").grid(row=0, column=1, pady=(1,0), padx=(5,0), sticky="W")
        ttk.Checkbutton(tagLabelFrame, text="meta", variable=self.div, onvalue="div", offvalue="").grid(row=1, column=1, pady=(1,0), padx=(5,0), sticky="W")
        

        self.tagEntry = ttk.Entry(tagLabelFrame, textvariable=self.addTag)
        self.tagEntry.grid(row=3, column=0, columnspan=2, padx=(5,0), pady=(8,0), sticky="NSEW")
        ttk.Button(tagLabelFrame, command=self.do_nothing, text="Add").grid(row=3, column=3, pady=(8,0), sticky="NSEW")
        self.tagEntry.bind("<FocusIn>", lambda event, arg=self.addTag: self.clean_example_text(event, arg))
        self.tagEntry.bind("<FocusOut>", lambda event, arg=[self.addTag, self.TAGENTRY]: self.check_entry(event, arg))

        self.class_atr = ttk.StringVar()
        self.id_attr = ttk.StringVar()
        self.style = ttk.StringVar()
        self.href = ttk.StringVar()

        self.addAttr = ttk.StringVar()
        self.addAttr.set(self.ATTRENTRY)
        attrLabelFrame = ttk.LabelFrame(self, text="Attributes", borderwidth=1)
        attrLabelFrame.grid(row=1, column=1, pady=10, padx=10, ipadx=5, ipady=5, sticky="NEWS")
        ttk.Checkbutton(attrLabelFrame, text="class", variable=self.class_atr, onvalue="head", offvalue="").grid(row=0, column=0, pady=(1,0), padx=(5,0), sticky="W")
        ttk.Checkbutton(attrLabelFrame, text="id", variable=self.id_attr, onvalue="id", offvalue="").grid(row=1, column=0, pady=(1,0), padx=(5,0), sticky="W")
        ttk.Checkbutton(attrLabelFrame, text="style", variable=self.style, onvalue="style", offvalue="").grid(row=2, column=0, pady=(1,0), padx=(5,0), sticky="W")
        ttk.Checkbutton(attrLabelFrame, text="href", variable=self.href, onvalue="href", offvalue="").grid(row=0, column=1, pady=(1,0), padx=(5,0), sticky="W")

        self.attrEntry = ttk.Entry(attrLabelFrame, textvariable=self.addAttr)
        self.attrEntry.grid(row=3, column=0, columnspan=2, padx=(5,0), pady=(8,0), sticky="NSEW")
        ttk.Button(attrLabelFrame, command=self.do_nothing, text="Add").grid(row=3, column=3, pady=(8,0), sticky="NSEW")
        self.attrEntry.bind("<FocusIn>", lambda event, arg=self.addAttr: self.clean_example_text(event, arg))
        self.attrEntry.bind("<FocusOut>", lambda event, arg=[self.addAttr, self.ATTRENTRY]: self.check_entry(event, arg))
    
    def check_entry(self, event, arg):
        if len(arg[0].get()) == 0:
            arg[0].set(arg[1])

    def do_nothing(self):
        print("DO NOTHING!")
    
    def clean_example_text(self, e, arg):
        arg.set('')

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
        self.__create_menu()

        self.input_frame = InputFrame(self)
        self.input_frame.grid(column=0, row=0, columnspan=4, sticky="WENS")

        self.listbox_frame = ListboxFrame(self)
        self.listbox_frame.grid(column=0, row=1, sticky="WENS", pady=(0, 5), padx=5)

        self.headers_frame = HeadersFrame(self)
        self.headers_frame.grid(column=0, row=2, sticky="WENS")

        self.options_frame = OptionsFrame(self)
        self.options_frame.grid(column=1, row=0, rowspan=8, sticky=ttk.W+ttk.E, padx=(0,15))
    
    def __create_menu(self):
        menubar = ttk.Menu(self)
        
        file_menu = ttk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New", command=self.do_nothing)
        file_menu.add_command(label="Open", command=self.do_nothing)
        file_menu.add_command(label="Save", command=self.do_nothing)
        file_menu.add_command(label="Save as...", command=self.do_nothing)
        file_menu.add_command(label="Export Scrape", command=self.do_nothing)
        file_menu.add_separator()
        file_menu.add_command(label="Quit", command=self.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        
        edit_menu = ttk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Find", command=self.do_nothing)
        edit_menu.add_separator()
        edit_menu.add_command(label="Configure Headers", command=self.do_nothing)
        edit_menu.add_command(label="Configure Scraper", command=self.do_nothing)
        menubar.add_cascade(label="Edit", menu=edit_menu)

        help_menu = ttk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.do_nothing)
        menubar.add_cascade(label="Help", menu=help_menu)

        self.config(menu=menubar)
  
    
    def do_nothing(self):
        print("NOTHING!")


if __name__ == "__main__":
    app = ApplicationGUI()
    Manager(app)
    app.mainloop()