import gi
import Mkbib.pybib as pybib
import Mkbib.view as view
import Mkbib.dialogue as dialogue
import io
import Mkbib.cell as cell
import Mkbib.filemanager as filemanager
import os
from gi.repository import Gtk
gi.require_version("Gtk", "3.0")


class MenuManager(Gtk.Window):

    def __init__(self):
        self.parsing = pybib.parser()
        self.TreeView = view.treeview()
        self.Dialog = dialogue.FileDialog()
        self.cell = cell.cell_renderer()
        self.Files = filemanager.file_manager()

    def file_new_clicked(self, widget):
        dialog = Gtk.FileChooserDialog("Open an existing fine", None,
                                       Gtk.FileChooserAction.OPEN,
                                       (Gtk.STOCK_CANCEL,
                                        Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.filename = dialog.get_filename()
            return(self.filename)
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()

    def create_textview(self, SimpleAction, parameter):
        popup = Gtk.Window(border_width=5)
        popup.set_title("Add a complete bibtex entry")
        popup.set_default_size(350, 350)
        grid = Gtk.Grid()
        scrolw = Gtk.ScrolledWindow()
        scrolw.set_hexpand(True)
        scrolw.set_vexpand(True)
        button = Gtk.Button("Create")
        tview = Gtk.TextView()
        tview.set_wrap_mode(Gtk.WrapMode.WORD)

        # Get the buffer
        textbuffer = tview.get_buffer()
        scrolw.add(tview)
        grid.attach(scrolw, 0,  0, 10, 10)
        grid.attach(button, 0, 11, 10,  1)
        button.connect("clicked", self.create_from_buffer, textbuffer, popup)
        popup.add(grid)
        popup.show_all()

    def create_from_buffer(self, widget, textbuffer, window):
        start_iter = textbuffer.get_start_iter()
        end_iter = textbuffer.get_end_iter()
        text = io.StringIO(textbuffer.get_text(start_iter,
                                                    end_iter, True))
        del self.parsing.booklist[:]
        self.parsing.parsing_read(text)
        self.TreeView.viewer(self.parsing.booklist)
        window.destroy()
