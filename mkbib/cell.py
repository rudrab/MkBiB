import gi
import os
import webbrowser
import dialogue

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class cell_renderer():
    # slist = ""
    def __init__(self):
        self.dialogue = dialogue.MessageDialog()
        rootdir = "/var/tmp"
        basedir = rootdir+"/Mkbib"
        if not os.path.exists(basedir):
            os.makedirs(basedir)

    def open_from_renderer(self):
        dxurl = "http://dx.doi.org/"
        # print(self.slist)
        try:
            url = dxurl+self.slist
            webbrowser.open(url)
        except:
            print("DOI is not available")
            self.dialogue.on_warn_clicked("DOI is not given", "Search google instead")

    def row_activated(self, widget, row, col):
        self.row = row
        model = widget.get_model()
        indx = str(model[row][0])
        self.slist = model[row][0:][-1]
        # print(slist[-1])
        return(self.slist)

# cell_renderer.open_from_renderer()
