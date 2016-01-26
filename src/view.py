import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

booklist = []
class treeview():
    bookstore = Gtk.ListStore(int, str, str, str, str, str, str,str, str,
                              str, str, str,str, str, str, str, str,
                              str, str, str, str, str,str, str, str, str, str)
    view = Gtk.TreeView(model=bookstore)

    def viewer(self, booklist):
        # print(booklist)
        for ref in booklist:
            self.bookstore.append(list(ref))
        self.current_filter_language = None
        for i, column_title in enumerate(["Index", "Type", "Key", "Title",
                                          "Author", "Publishers", "Year"]):
            renderer = Gtk.CellRendererText()
            renderer.set_property("wrap-width", 400)
            if i > 4:
                renderer.set_property("wrap-width", 150)
            renderer.set_property("wrap-mode", 0)
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.view.append_column(column)
            for cid in range(0,6):
                column.set_sort_column_id(cid)
        # print("view working")
        # self.view_status = True

    def compare(model, row1, row2, user_data):
        sort_column, _ = model.get_sort_column_id()
        value1 = model.get_value(row1, sort_column)
        value2 = model.get_value(row2, sort_column)
        if value1 < value2:
            return -1
        elif value1 == value2:
            return 0
        else:
            return 1
