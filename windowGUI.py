import tkinter as ttk
import tkinter.filedialog as openFile
from Eparser import Eparser

class Manager(object):
    def __init__(self, gui):
       self.parser = Eparser()
       self.gui = gui
       self.gui.listbox_frame.manager = self
       self.gui.button_frame.manager = self

    def setEntry(self, filename):
        self.gui.input_frame.urlFileName.set(filename)
    
    def btnScrape(self):
        fileORhttp = self.gui.input_frame.urlFileName.get()
        if len(fileORhttp) < 5:
            print("Not a file or a url!")
        else:
            if fileORhttp[0:4] == ("http"):
                print("DO SOMETHING WITH WEBSITE")
            else:
                f = open(fileORhttp, 'r', encoding='utf-8')
                requestBytes = f.read()
                #requestString = requestBytes.decode("utf-8")
                self.parser.feed(requestBytes)
                f.close()
            for t in self.parser.htmlDoc.keys():
                self.gui.listbox_frame.tagListbox.insert(ttk.END, t)
    
class InputFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.__create_widgets()
    
    def __create_widgets(self):
        self.urlFile = ttk.Label(self, text = "Url / File:").grid(column=0, row=0, sticky=ttk.W)
        self.urlFileName = ttk.StringVar()
        self.urlFileEntry = ttk.Entry(self, width=100, textvariable = self.urlFileName)
        self.urlFileEntry.focus()
        self.urlFileEntry.grid(column=1, row=0, sticky=ttk.W)
        for widget in self.winfo_children():
            widget.grid(padx=0, pady=5)

class ButtonFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.columnconfigure(0, weight=1)
        self.__create_widgets()
        self.manager = None

    def __create_widgets(self):
        self.scrapeBtn = ttk.Button(self, text="Scrape", command=self.btnScrape, underline=0).grid(column=0, row=0, ipadx=3)
        self.openFile = ttk.Button(self, text="Open file..", command=self.btnOpenFile, underline=0).grid(column=1, row=0, ipadx=3)
        for widget in self.winfo_children():
            widget.grid(padx=3, pady=3)
    
    def btnScrape(self):
        self.manager.btnScrape()

    def btnOpenFile(self):
        filename = openFile.askopenfilename(initialdir="/", title="Select file", filetypes=[('HTML', '*.html')])
        self.manager.setEntry(filename)


class ListboxFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.__create_widgets()
        self.manager = None
        self.selected = { 'tag': None, 'attr': None }
    
    def __create_widgets(self):
        self.tagFrame = ttk.Label(self, text = "Tags").grid(row=0, column=0, sticky=ttk.S+ttk.E+ttk.W+ttk.N)

        # TAG SCROLL AND LISTBOX #
        self.tagScrollbar = ttk.Scrollbar(self, orient=ttk.VERTICAL)
        self.tagScrollbar.grid(row=1, column=1, sticky=ttk.N+ttk.S)

        self.tagListbox = ttk.Listbox(self, yscrollcommand=self.tagScrollbar.set)
        self.tagListbox.grid(row=1, column=0, sticky=ttk.S+ttk.E+ttk.W+ttk.N)

        self.tagListbox.bind("<<ListboxSelect>>", self.updateAttrListbox)
        

        self.tagListbox.columnconfigure(0, weight=1)

        # ATTR SCROLL AND LISTBOX
        self.attrFrame = ttk.Label(self, text = "Attributes").grid(row=0, column=2, sticky=ttk.S+ttk.E+ttk.W+ttk.N)
        self.attrScrollbar = ttk.Scrollbar(self, orient=ttk.VERTICAL)
        self.attrScrollbar.grid(row=1, column=3, sticky=ttk.N+ttk.S)

        self.attrListbox = ttk.Listbox(self, yscrollcommand=self.attrScrollbar.set)
        self.attrListbox.grid(row=1, column=2, sticky=ttk.S+ttk.E+ttk.W+ttk.N)
        
        self.attrListbox.columnconfigure(0, weight=1)

        self.tagScrollbar['command'] = self.tagListbox.yview
        self.attrScrollbar['command'] = self.attrListbox.yview
    
    def updateAttrListbox(self, e):
        self.selected['tag'] = self.tagListbox.get(self.tagListbox.curselection())
        self.attrListbox.delete(0, self.attrListbox.size())
        for a in self.manager.parser.htmlDoc[self.selected['tag']].keys():
            self.attrListbox.insert(ttk.END, a)


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

        self.columnconfigure(0, weight=4)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)

        self.__create_widgets()
    
    def __create_widgets(self):
        self.input_frame = InputFrame(self)
        self.input_frame.grid(column=0, row=0, sticky="WENS")

        self.button_frame = ButtonFrame(self)
        self.button_frame.grid(column=1, row=0, sticky="WENS")

        self.listbox_frame = ListboxFrame(self)
        self.listbox_frame.grid(row=1, column=0, sticky="WENS", padx=5, pady=(0, 5))


if __name__ == "__main__":
    app = ApplicationGUI()
    Manager(app)
    app.mainloop()