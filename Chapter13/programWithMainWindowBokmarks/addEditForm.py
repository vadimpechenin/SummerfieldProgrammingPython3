import tkinter

class AddEditForm(tkinter.Toplevel):

    def __init__(self, parent, name=None, url=None):
        super().__init__(parent)
        self.parent = parent
        self.accepted = False
        self.transient(self.parent)
        self.title("Bookmarks - " + (
                   "Edit" if name is not None else "Add"))

        self.nameVar = tkinter.StringVar()
        if name is not None:
            self.nameVar.set(name)
        self.urlVar = tkinter.StringVar()
        self.urlVar.set(url if url is not None else "http://")

        frame = tkinter.Frame(self)
        nameLabel = tkinter.Label(frame, text="Name:", underline=0)
        nameEntry = tkinter.Entry(frame, textvariable=self.nameVar)
        nameEntry.focus_set()
        urlLabel = tkinter.Label(frame, text="URL:", underline=0)
        urlEntry = tkinter.Entry(frame, textvariable=self.urlVar)
        okButton = tkinter.Button(frame, text="OK", command=self.ok)
        cancelButton = tkinter.Button(frame, text="Cancel",
                                      command=self.close)

        nameLabel.grid(row=0, column=0, sticky=tkinter.W, pady=3,
                       padx=3)
        nameEntry.grid(row=0, column=1, columnspan=3,
                       sticky=tkinter.EW, pady=3, padx=3)
        urlLabel.grid(row=1, column=0, sticky=tkinter.W, pady=3,
                      padx=3)
        urlEntry.grid(row=1, column=1, columnspan=3,
                      sticky=tkinter.EW, pady=3, padx=3)
        okButton.grid(row=2, column=2, sticky=tkinter.EW, pady=3,
                      padx=3)
        cancelButton.grid(row=2, column=3, sticky=tkinter.EW, pady=3,
                          padx=3)

        frame.grid(row=0, column=0, sticky=tkinter.NSEW)
        frame.columnconfigure(1, weight=1)
        window = self.winfo_toplevel()
        window.columnconfigure(0, weight=1)

        self.bind("<Alt-n>", lambda *ignore: nameEntry.focus_set())
        self.bind("<Alt-u>", lambda *ignore: urlEntry.focus_set())
        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.close)

        self.protocol("WM_DELETE_WINDOW", self.close)
        self.grab_set()
        self.wait_window(self)


    def ok(self, event=None):
        self.name = self.nameVar.get()
        self.url = self.urlVar.get()
        self.accepted = True
        self.close()


    def close(self, event=None):
        self.parent.focus_set()
        self.destroy()
