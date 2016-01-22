import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, Pango

class treeview():
    def __init__(self):
    # def viewer(self, booklist):
        booklist = []
        # filename = "mkBiB"
        # filename = MenuElem.file_open_clicked(filename)
        # hb = Gtk.HeaderBar()
        # hb.set_show_close_button(True)
        # hb.props.title = filename
        # self.set_titlebar(hb)
        # parsing.parsing_read(filename, booklist)
        self.bookstore = Gtk.ListStore(int, str, str, str, str)
        for ref in booklist:
            self.bookstore.append(list(ref))
        self.current_filter_language = None
        self.view = Gtk.TreeView(model=self.bookstore)
        for i, column_title in enumerate(["Index", "Title", "Author",
                                          "Publishers", "Year"]):
            renderer = Gtk.CellRendererText()
            renderer.set_property("wrap-width", 400)
            if i > 2:
                renderer.set_property("wrap-width", 150)
            renderer.set_property("wrap-mode", 0)
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.view.append_column(column)
        print("view working")
