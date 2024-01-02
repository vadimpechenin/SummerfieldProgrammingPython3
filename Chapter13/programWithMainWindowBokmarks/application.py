"""
Программа запуска простой диалоговой программы Interest
"""
import os
import sys
import tkinter

from programWithMainWindowBokmarks.mainWindow import MainWindow

application = tkinter.Tk()
path = os.path.join(os.path.dirname(__file__), "images/")
if sys.platform.startswith("win"):
    icon = path + "bookmark.ico"
else:
    icon = "@" + path + "bookmark.xbm"
application.iconbitmap(icon)
window = MainWindow(application)
application.protocol("WM_DELETE_WINDOW", window.fileQuit)
application.mainloop()