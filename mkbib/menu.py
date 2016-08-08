import gi
import pybib
import view
import dialogue
import io
import cell
import filemanager
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
        # self.add_filters(dialog)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.filename = dialog.get_filename()
            return(self.filename)
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()

    def file_open_clicked(self, name, action):
        self.Dialog.FileChooser(["Open Existing BiBTeX File",
                                 "BiBTeX File", "*.bib"],
                                Gtk.FileChooserAction.OPEN)
        if self.Dialog.response == Gtk.ResponseType.OK:
            filename = self.Dialog.dialog.get_filename()
            self.Dialog.dialog.destroy()
            del self.parsing.booklist[:]
            self.TreeView.bookstore.clear()
            self.TreeView.indxcount = 0
            with open(filename, "r") as fname:
                self.parsing.parsing_read(fname)
                self.Files.chk_subdir(os.path.splitext(os.path.basename(filename))[0])
            self.TreeView.viewer(self.parsing.booklist)
        elif self.Dialog.response == Gtk.ResponseType.CANCEL:
            self.Dialog.dialog.destroy()

    def file_save_as_clicked(self, name, action):
        self.Dialog.FileChooser(["Save as an existing file",
                                 "BiBTeX File", "*.bib"],
                                 Gtk.FileChooserAction.SAVE)
        if self.Dialog.response == Gtk.ResponseType.OK:
            filename = self.Dialog.dialog.get_filename()
            print(filename)
            self.parsing.parsing_write(filename)
            self.Dialog.dialog.destroy()
        elif self.Dialog.response == Gtk.ResponseType.CANCEL:
            self.Dialog.dialog.destroy()

    def on_menu_file_quit(self, widget):
        Gtk.main_quit()

    # def on_menu_others(self, widget):
        # print("Menu item " + widget.get_name() + " was selected")

    # def on_menu_choices_changed(self, widget, current):
        # filename = current.get_name()+".xml"
        # print(filename + " will be opened")

    def create_textview(self, SimpleAction, parameter):
        self.popup = Gtk.Window(border_width=5)
        self.popup.set_title("Add a complete bibtex entry")
        self.popup.set_default_size(350, 350)
        grid = Gtk.Grid()
        scrolw = Gtk.ScrolledWindow()
        scrolw.set_hexpand(True)
        scrolw.set_vexpand(True)
        button = Gtk.Button("Create")
        button.connect("clicked", self.create_from_buffer)
        tview = Gtk.TextView()
        tview.set_wrap_mode(Gtk.WrapMode.WORD)

        # Get the buffer
        self.textbuffer = tview.get_buffer()
        scrolw.add(tview)
        grid.attach(scrolw, 0,  0, 10, 10)
        grid.attach(button, 0, 11, 10,  1)
        self.popup.add(grid)
        self.popup.show_all()

    def create_from_buffer(self, widget):
        start_iter = self.textbuffer.get_start_iter()
        end_iter = self.textbuffer.get_end_iter()
        text = io.StringIO(self.textbuffer.get_text(start_iter,
                                                    end_iter, True))
        del self.parsing.booklist[:]
        self.parsing.parsing_read(text)
        self.TreeView.viewer(self.parsing.booklist)
        self.popup.destroy()
