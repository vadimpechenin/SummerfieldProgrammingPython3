import os
import pickle
import tkinter
import tkinter.filedialog
import tkinter.messagebox
import webbrowser

from programWithMainWindowBokmarks.addEditForm import AddEditForm


class MainWindow:

    def __init__(self, parent):
        self.parent = parent

        self.filename = None
        self.dirty = False
        self.data = {}

        menubar = tkinter.Menu(self.parent)
        self.parent["menu"] = menubar

        fileMenu = tkinter.Menu(menubar)
        for label, command, shortcut_text, shortcut in (
                ("New...", self.fileNew, "Ctrl+N", "<Control-n>"),
                ("Open...", self.fileOpen, "Ctrl+O", "<Control-o>"),
                ("Save", self.fileSave, "Ctrl+S", "<Control-s>"),
                (None, None, None, None),
                ("Quit", self.fileQuit, "Ctrl+Q", "<Control-q>")):
            if label is None:
                fileMenu.add_separator()
            else:
                fileMenu.add_command(label=label, underline=0,
                                     command=command, accelerator=shortcut_text)
                self.parent.bind(shortcut, command)
        menubar.add_cascade(label="File", menu=fileMenu, underline=0)

        editMenu = tkinter.Menu(menubar)
        for label, command, shortcut_text, shortcut in (
                ("Add...", self.editAdd, "Ctrl+A", "<Control-a>"),
                ("Edit...", self.editEdit, "Ctrl+E", "<Control-e>"),
                ("Delete...", self.editDelete, "Delete", "<Delete>"),
                (None, None, None, None),
                ("Show Web Page...", self.editShowWebPage, "Ctrl+W",
                 "<Control-w>")):
            if label is None:
                editMenu.add_separator()
            else:
                editMenu.add_command(label=label, underline=0,
                                     command=command, accelerator=shortcut_text)
                self.parent.bind(shortcut, command)
        menubar.add_cascade(label="Edit", menu=editMenu, underline=0)

        frame = tkinter.Frame(self.parent)
        self.toolbar_images = []
        toolbar = tkinter.Frame(frame)
        for image, command in (
                ("images/filenew.gif", self.fileNew),
                ("images/fileopen.gif", self.fileOpen),
                ("images/filesave.gif", self.fileSave),
                ("images/editadd.gif", self.editAdd),
                ("images/editedit.gif", self.editEdit),
                ("images/editdelete.gif", self.editDelete),
                ("images/editshowwebpage.gif", self.editShowWebPage)):
            image = os.path.join(os.path.dirname(__file__), image)
            try:
                image = tkinter.PhotoImage(file=image)
                self.toolbar_images.append(image)
                button = tkinter.Button(toolbar, image=image,
                                        command=command)
                button.grid(row=0, column=len(self.toolbar_images) - 1)
            except tkinter.TclError as err:
                print(err)
        toolbar.grid(row=0, column=0, columnspan=2, sticky=tkinter.NW)

        scrollbar = tkinter.Scrollbar(frame, orient=tkinter.VERTICAL)
        self.listBox = tkinter.Listbox(frame,
                                       yscrollcommand=scrollbar.set)
        self.listBox.grid(row=1, column=0, sticky=tkinter.NSEW)
        self.listBox.focus_set()
        scrollbar["command"] = self.listBox.yview
        scrollbar.grid(row=1, column=1, sticky=tkinter.NS)

        self.statusbar = tkinter.Label(frame, text="Ready...",
                                       anchor=tkinter.W)
        self.statusbar.after(5000, self.clearStatusBar)
        self.statusbar.grid(row=2, column=0, columnspan=2,
                            sticky=tkinter.EW)

        frame.grid(row=0, column=0, sticky=tkinter.NSEW)

        frame.columnconfigure(0, weight=999)
        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(0, weight=1)
        frame.rowconfigure(1, weight=999)
        frame.rowconfigure(2, weight=1)

        window = self.parent.winfo_toplevel()
        window.columnconfigure(0, weight=1)
        window.rowconfigure(0, weight=1)

        self.parent.geometry("{0}x{1}+{2}+{3}".format(400, 500,
                                                      0, 50))
        self.parent.title("Bookmarks - Unnamed")

    def okayToContinue(self):
        if not self.dirty:
            return True
        reply = tkinter.messagebox.askyesnocancel(
            "Bookmarks - Unsaved Changes",
            "Save unsaved changes?", parent=self.parent)
        if reply is None:
            return False
        if reply:
            return self.fileSave()
        return True

    def setStatusBar(self, text, timeout=5000):
        self.statusbar["text"] = text
        if timeout:
            self.statusbar.after(timeout, self.clearStatusBar)

    def clearStatusBar(self):
        self.statusbar["text"] = ""


    def fileNew(self):
        if not self.okayToContinue():
            return
        self.listBox.delete(0, tkinter.END)
        self.dirty = False
        self.filename = None
        self.data = {}
        self.parent.title("Bookmarks - Unnamed")

    def fileOpen(self):
        if not self.okayToContinue():
            return
        dir = (os.path.dirname(self.filename)
               if self.filename is not None else ".")
        filename = tkinter.filedialog.askopenfilename(
            title="Bookmarks - Open File",
            initialdir=dir,
            filetypes=[("Bookmarks files", "*.bmf")],
            defaultextension=".bmf", parent=self.parent)
        if filename:
            self.loadFile(filename)

    def loadFile(self, filename):
        self.filename = filename
        self.listBox.delete(0, tkinter.END)
        self.dirty = False
        try:
            with open(self.filename, "rb") as fh:
                self.data = pickle.load(fh)
            for name in sorted(self.data, key=str.lower):
                self.listBox.insert(tkinter.END, name)
            self.setStatusBar("Loaded {0} bookmarks from {1}".format(
                self.listBox.size(), self.filename))
            self.parent.title("Bookmarks - {0}".format(
                os.path.basename(self.filename)))
        except (EnvironmentError, pickle.PickleError) as err:
            tkinter.messagebox.showwarning("Bookmarks - Error",
                                           "Failed to load {0}:\n{1}".format(
                                               self.filename, err), parent=self.parent)


    def fileSave(self):
        if self.filename is None:
            filename = tkinter.filedialog.asksaveasfilename(
                title="Bookmarks - Save File",
                initialdir=".",
                filetypes=[("Bookmarks files", "*.bmf")],
                defaultextension=".bmf",
                parent=self.parent)
            if not filename:
                return False
            self.filename = filename
            if not self.filename.endswith(".bmf"):
                self.filename += ".bmf"
        try:
            with open(self.filename, "wb") as fh:
                pickle.dump(self.data, fh, pickle.HIGHEST_PROTOCOL)
            self.dirty = False
            self.setStatusBar("Saved {0} items to {1}".format(
                len(self.data), self.filename))
            self.parent.title("Bookmarks - {0}".format(
                os.path.basename(self.filename)))
        except (EnvironmentError, pickle.PickleError) as err:
            tkinter.messagebox.showwarning("Bookmarks - Error",
                                           "Failed to save {0}:\n{1}".format(
                                               self.filename, err), parent=self.parent)
        return True

    def editAdd(self, *ignore):
        form = AddEditForm(self.parent)
        if form.accepted and form.name:
            self.data[form.name] = form.url
            self.listBox.delete(0, tkinter.END)
            for name in sorted(self.data, key=str.lower):
                self.listBox.insert(tkinter.END, name)
            self.dirty = True

    def editEdit(self, *ignore):
        indexes = self.listBox.curselection()
        if not indexes or len(indexes) > 1:
            return
        index = indexes[0]
        name = self.listBox.get(index)
        form = AddEditForm(self.parent, name, self.data[name])
        if form.accepted and form.name:
            self.data[form.name] = form.url
            if form.name != name:
                del self.data[name]
                self.listBox.delete(0, tkinter.END)
                for name in sorted(self.data, key=str.lower):
                    self.listBox.insert(tkinter.END, name)
            self.dirty = True

    def editDelete(self, *ignore):
        indexes = self.listBox.curselection()
        if not indexes or len(indexes) > 1:
            return
        index = indexes[0]
        name = self.listBox.get(index)
        if tkinter.messagebox.askyesno("Bookmarks - Delete",
                                       "Delete '{0}'?".format(name)):
            self.listBox.delete(index)
            self.listBox.focus_set()
            del self.data[name]
            self.dirty = True

    def editShowWebPage(self, *ignore):
        indexes = self.listBox.curselection()
        if not indexes or len(indexes) > 1:
            return
        index = indexes[0]
        url = self.data[self.listBox.get(index)]
        webbrowser.open_new_tab(url)

    def fileQuit(self, event=None) -> None:
        if self.okayToContinue():
            self.parent.destroy()

    def okayToContinue(self):
        if not self.dirty:
            return True
        reply = tkinter.messagebox.askyesnocancel(
            "Bookmarks - Unsaved Changes",
            "Save unsaved changes?", parent=self.parent)
        if reply is None:
            return False
        if reply:
            return self.fileSave()
        return True