import gi
import os
import webbrowser
import Mkbib.dialogue as dialogue
from gi.repository import Gtk
gi.require_version("Gtk", "3.0")


class cell_renderer():
    # slist = ""
    def __init__(self):
        self.Messages = dialogue.MessageDialog()
        self.Dialog = dialogue.FileDialog()

    # def open_from_renderer(self):
    def search_doi(self, doi):
        dxurl = "http://dx.doi.org/"
        # print(self.slist)
        try:
            url = dxurl+doi
            webbrowser.open(url)
        except:
            print("DOI is not available")
            self.Messages.on_warn_clicked("DOI is not given",
                                          "Search google instead")

    def row_activated(self, widget, row, col):
        self.row = row
        model = widget.get_model()
        indx = str(model[row][0])
        self.doi = model[row][0:][-2]
        self.doc = model[row][0:][-1]

    def file_attach_cb(self):
        self.Dialog.FileChooser(["Open Pdf file", "PDF File", "*.pdf"], Gtk.FileChooserAction.OPEN, Gtk.STOCK_OPEN)
        if self.Dialog.response == Gtk.ResponseType.OK:
            self.file_name = self.Dialog.dialog.get_filename()
            self.Dialog.dialog.destroy()
        elif self.Dialog.response == Gtk.ResponseType.CANCEL:
            self.Dialog.dialog.destroy()
        return self.file_name
