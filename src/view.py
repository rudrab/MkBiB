import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

booklist = []
class treeview():
    view_status = False
    bookstore = Gtk.ListStore(int, str, str, str, str)
    view = Gtk.TreeView(model=bookstore)
    def viewer(self, booklist):
        # print(booklist)
        for ref in booklist:
            self.bookstore.append(list(ref))
        self.current_filter_language = None
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
        self.view_status = True
