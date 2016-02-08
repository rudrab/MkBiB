import gi
import pybib
import view
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class MenuManager:#(Gtk.UIManager):

    def __init__(self):
        self.parsing = pybib.parser()
        self.TreeView = view.treeview()

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

    def file_open_clicked(self, SimpleAction, parameter):
        dialog = Gtk.FileChooserDialog("Open an existing fine", None,
                                       Gtk.FileChooserAction.OPEN,
                                       (Gtk.STOCK_CANCEL,
                                        Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        filter = Gtk.FileFilter()
        filter.set_name("BiBTex File")
        filter.add_pattern("*.bib")
        dialog.add_filter(filter)
        filter = Gtk.FileFilter()
        filter.set_name("All Files")
        filter.add_pattern("*")
        dialog.add_filter(filter)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            filename = dialog.get_filename()
            dialog.destroy()
            self.TreeView.bookstore.clear()
            global indxcount
            indxcount = 0
            self.parsing.parsing_read(filename)
            self.TreeView.viewer(self.parsing.booklist)
            # self.TreeView.view.set_model()
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")
            dialog.destroy()

    def file_save_clicked(self, widget):
        dialog = Gtk.FileChooserDialog("Save as an existing file", None,
                                       Gtk.FileChooserAction.SAVE,
                                       (Gtk.STOCK_CANCEL,
                                        Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_SAVE, Gtk.ResponseType.OK))
        # self.add_filters(dialog)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            filename = dialog.get_filename()
            self.parsing.parsing_write(filename)
            # return(self.filename)
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")
        dialog.destroy()

    def on_menu_file_quit(self, widget):
        Gtk.main_quit()

    def on_menu_others(self, widget):
        print("Menu item " + widget.get_name() + " was selected")

    def on_menu_choices_changed(self, widget, current):
        filename = current.get_name()+".xml"
        print(filename + " will be opened")
