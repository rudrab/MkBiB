import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import cell

class treeview():
    full_list = []
    booklist = []
    indxcount = 0
    bookstore = Gtk.ListStore(int, str, str, str, str, str, str, str, str, str,
                              str, str, str, str, str, str, str, str, str, str,
                              str, str, str, str, str, str, str, str)
    viewstore = Gtk.ListStore(str, str)
    entries = ["Type", "Id", "Title", "Author", "Journal", "Year", "Publisher",
               "Page", "Address", "Annote", "Booktitle", "Chapter", "Crossred",
               "Edition", "Editor", "Howpublished", "Institution", "Month",
               "Note", "Number", "Organization", "Pages", "School", "Series",
               "Type", "Volume", "DOI"]

    def __init__(self):
        self.cell = cell.cell_renderer()
        self.view = Gtk.TreeView(model=self.bookstore)
# Put all crc edit inside this block
        liststore_props = Gtk.ListStore(str)
        props = ["Open", "Edit", "Webpage","Delete"]
        for item in props:
            liststore_props.append([item])

        renderer_combo = Gtk.CellRendererCombo()
        renderer_combo.set_property("editable", True)
        renderer_combo.set_property("model", liststore_props)
        renderer_combo.set_property("text-column", 0)
        renderer_combo.set_property("has-entry", False)
        renderer_combo.connect("edited", self.on_combo_changed)
        column_combo = Gtk.TreeViewColumn("Index", renderer_combo, text=0)
        self.view.append_column(column_combo)
# This is crc block

        for i, column_title in enumerate(["Type", "Key", "Title",
                                          "Author", "Journal", "Year"]):
            renderer = Gtk.CellRendererText()
            renderer.set_property("wrap-width", 300)
            if i > 3:
                renderer.set_property("wrap-width", 100)
            renderer.set_property("wrap-mode", 0)
            column = Gtk.TreeViewColumn(column_title, renderer, text=i+1)
            self.view.append_column(column)
            # column.clear()
            for cid in range(0, 6):
                column.set_sort_column_id(cid)
        self.view.connect("row-activated", self.row_activated)

    def on_combo_changed(self, widget, path, text):
        self.bookstore[path][7] = text
        self.cell.row_activated(self.view, str(int(self.bookstore[path][0])-1), 0)
        if text == "Open":
            self.cell.open_from_renderer()
        elif text == "Edit":
            self.row_activated(self.view, str(int(self.bookstore[path][0])-1), 0)
        elif text == "Delete":
            (model, iter) = self.view.get_selection().get_selected()
            self.bookstore.remove(iter)
        else:
            print("Wait")


    def viewer(self, booklist, act=-1):
        for ref in booklist:
            lref = list(ref)
            treeview.indxcount += 1
            lref = list(ref)
            lref.insert(0, (treeview.indxcount))

            if act == -1:
                self.bookstore.append(lref)
                treeview().full_list.append(ref)
            else:
                try:
                    self.bookstore.insert_before(act, lref)
                    indx = int(self.bookstore.get_string_from_iter(act))
                    treeview().full_list[indx] = ref
                except TypeError:
                    self.bookstore.append(lref)
                    treeview().full_list[-1] = ref

        self.current_filter_language = None
        # print(treeview.full_list)


    def row_activated(self, widget, row, col):
        self.row = row
        model = widget.get_model()
        indx = str(model[row][0])
        slist = list(zip(self.entries, model[row][1:]))
        self.retrieve_treeview(slist, indx)
        # print(slist[-1][-1])
        # self.treeview.remove(row)
        return True

    def update_list(self, tuples):
        self.booklist.append(tuples)
        # self.viewer(self.booklist)
        # return(self.booklist)

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

    def retrieve_treeview(self, slist, indx):
        self.popup = Gtk.Window()
        self.popup.set_border_width(2)
        popheader = Gtk.HeaderBar()
        self.popup.set_titlebar(popheader)
        popheader.set_title(indx)
        self.popup.set_default_size(450, 550)
        popheader.set_show_close_button(True)
        spinner = Gtk.Spinner()
        popheader.pack_end(spinner)
        spinner.start()

        grid = Gtk.Grid()
        scrolw = Gtk.ScrolledWindow()
        scrolw.set_hexpand(True)
        scrolw.set_vexpand(True)
        self.updater = Gtk.Button("Update")
        self.updater.connect("clicked", self.edit_and_save_buffer)
        self.updater.set_sensitive(False)
        tview = Gtk.TreeView(model=self.viewstore)
        self.viewstore.clear()
        for i, viewcol in enumerate(["Key", "Value"]):
            vrenderer = Gtk.CellRendererText()
            if i == 1:
                vrenderer.set_property("wrap-width", 300)
                vrenderer.set_property("editable", True)
            vcolumn = Gtk.TreeViewColumn(viewcol, vrenderer, text=i)
            tview.append_column(vcolumn)
        vrenderer.connect("edited", self.val_edited)
        self.slist = slist
        # del slist
        for keyval in self.slist:
            self.viewstore.append(list(keyval))
        scrolw.add(tview)
        grid.attach(scrolw, 0,  0, 10, 10)
        grid.attach(self.updater, 0, 11, 10,  1)
        self.popup.add(grid)
        self.popup.show_all()

    def val_edited(self, widget, path, text):
        self.viewstore[path][1] = text
        # print("TexT"+text)
        self.val_list = [i[1] for i in self.slist]
        self.val_list[int(path)] = text
        # print(self.val_list)
        self.updater.set_sensitive(True)

    def edit_and_save_buffer(self, widget):
        val_tuple = tuple(self.val_list)
        val_ltup = [val_tuple]
        del val_tuple
        (model, iter) = self.view.get_selection().get_selected()
        if iter is not None:
            self.bookstore.remove(iter)
            self.viewer(val_ltup, act=iter)
        else:
            print("Cant Remove")
        del self.slist
        del self.val_list
        del val_ltup
        self.popup.destroy()
