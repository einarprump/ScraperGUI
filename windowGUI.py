import tkinter as ttk
import tkinter.filedialog as openFile
from Eparser import Eparser

class Manager(object):
    def __init__(self, gui):
       self.parser = Eparser()
       self.gui = gui
       self.gui.button_frame.manager = self

    def setEntry(self, asdf):
        self.gui.input_frame.urlFileName.set(asdf)
    
    def btnScrape(self):
        fileORhttp = self.gui.input_frame.urlFileName.get()
        if fileORhttp[0:5] == ("http:"):
            print("DO SOMETHING WITH WEBSITE")
        else:
            f = open(fileORhttp, 'r', encoding='utf-8')
            requestBytes = f.read()
            #requestString = requestBytes.decode("utf-8")
            self.parser.feed(requestBytes)
            f.close()

        for t in self.parser.htmlDoc.keys():
            self.gui.tag_frame.tagListbox.insert(ttk.END, t)
    
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


class TagFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.__create_widgets()
    
    def __create_widgets(self):
        self.tagFrame = ttk.Label(self, text = "Tags").grid(row=0, column=0, sticky=ttk.S+ttk.E+ttk.W+ttk.N)

        self.tagScrollbar = ttk.Scrollbar(self, orient=ttk.VERTICAL)
        self.tagScrollbar.grid(row=1, column=1, sticky=ttk.N+ttk.S)

        self.tagListbox = ttk.Listbox(self, yscrollcommand=self.tagScrollbar)
        self.tagListbox.grid(row=1, column=0, sticky=ttk.S+ttk.E+ttk.W+ttk.N)


        #self.tagListbox.bind("<<ListboxSelect>>", self.updateTagSelected)  
        self.tagListbox.columnconfigure(0, weight=1)

        self.tagScrollbar['command'] = self.tagListbox.yview


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

        self.tag_frame = TagFrame(self)
        self.tag_frame.grid(row=1, column=0, sticky="WENS", padx=5, pady=(0, 5))


if __name__ == "__main__":
    app = ApplicationGUI()
    Manager(app)
    app.mainloop()