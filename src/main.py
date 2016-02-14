import gi
import sys
import menu
import view
from gi.repository import Gtk, Gio  # , GLib, Gdk
gi.require_version("Gtk", "3.0")


class Window(Gtk.ApplicationWindow):
    def __init__(self, application, giofile=None):
        Gtk.ApplicationWindow.__init__(self,
                                       application=application,
                                       default_width=1000,
                                       default_height=200,
                                       title="mkbib")

        self.TreeView = view.treeview()
        self.MenuElem = menu.MenuManager()
        # New Menu
        action = Gio.SimpleAction(name="save")
        action.connect("activate", self.MenuElem.file_save_clicked)
        self.add_action(action)

        # Open menu
        action = Gio.SimpleAction(name="open")
        action.connect("activate", self.MenuElem.file_open_clicked)
        self.add_action(action)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        # box.pack_start(MenuElem.menubar, False, False, 0)
        self.add(box)
        self.TreeView = view.treeview()

        # Generate Entry type
        key_store = Gtk.ListStore(int, str)
        keys = ["Article", "Book", "Booklet", "Conference", "inBook",
                "inCollection", "inProseedings", "Manual", "MasterThesis",
                "Misc", "PhdThesis", "Proceedings", "TechReport",
                "Unpublished"]
        for key in keys:
            key_store.append([keys.index(key), key])

        self.key_combo = Gtk.ComboBox.new_with_model_and_entry(key_store)
        self.key_combo.set_entry_text_column(1)

        # BibTeX Key
        self.KeyEntry = Gtk.Entry()
        self.KeyEntry.set_placeholder_text("BibtexKey")

        #  Generate the  Fields
        self.notebook = Gtk.Notebook()
        xpos = 0
        minf = 0
        self.all_fields = dict()
        self.fields = ["Author",  "Year",  "Journal", "Title", "Publisher",
                       "Page", "Address", "Annote", " Booktitle", "Chapter",
                       "Crossred", "Edition", "Editor", "HowPublished",
                       "Institution", "Month", "Note", "Number",
                       "Organization", "Pages", "Publishers", "School",
                       "Series", "Type"]
        Tabs = ["Essential", "Publishers", "Extra I", "Extra II"]
        for note in range(int(len(self.fields)/6)):
            ypos = 0
            self.npage = "page"+str(note)
            self.npage = Gtk.Grid()
            self.npage.set_border_width(10)
            maxf = minf+6
            for field in self.fields[minf:maxf]:
                self.lfield = "L" + field
                self.lfield = Gtk.Label(field)
                self.all_fields[field] = Gtk.Entry()
                self.all_fields[field].set_placeholder_text(field)
                self.npage.attach(self.lfield, xpos, ypos, 2, 1)
                self.npage.attach_next_to(self.all_fields[field], self.lfield,
                                          Gtk.PositionType.RIGHT, 1, 1)
                ypos += 1

            self.notebook.append_page(self.npage, Gtk.Label(Tabs[note]))
            minf = maxf

        # Create the buttons to get data
        bcreate = Gtk.Button("Create")
        bcreate.connect("clicked", self.get_data)
        bsearch = Gtk.Button("Search Google")

        scroll = Gtk.ScrolledWindow()
        scroll.set_hexpand(False)
        scroll.set_vexpand(True)

        grid = Gtk.Grid()
        grid.set_column_spacing(10)
        grid.attach(self.key_combo, 0, 0, 6, 2)
        grid.attach(self.KeyEntry, 8, 0, 4, 2)
        grid.attach(self.notebook, 0, 2, 12, 12)
        grid.attach(scroll, 15, 0, 105, 21)
        grid.attach(bcreate, 0, 14,  4, 1)
        grid.attach(bsearch, 8, 14,  4, 1)
        box.pack_start(grid, False, False, 0)
        scroll.add(self.TreeView.view)
        self.show_all()

    def get_data(self, widget):
        tree_iter = self.key_combo.get_active_iter()
        if tree_iter is not None:
            model = self.key_combo.get_model()
            row_id, name = model[tree_iter][:2]
        else:
            entry = self.key_combo.get_child()
            name = entry.get_text()

        neworder = [3, 0, 2, 1, 4, 5, 6, 7, 8, 9, 10, 11, 12,
                    13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
        fields = [self.fields[i] for i in neworder]
        datalist = []
        # datadict = {}
        datatup = tuple([name] + [self.KeyEntry.get_text()] +
                        [self.all_fields[field].get_text() or None
                         for field in fields])
        # print(datatup)
        # datadict = dict(zip(fields, datatup))
        # print(datadict)
        datalist.append(datatup)
        self.TreeView.viewer(datalist)
        print(datalist)

class mkbib(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(self)
        self.connect("startup", self.startup)
        self.connect("activate", self.activate)

    def about_activated(self, action, data=None):
        dialog = Gtk.AboutDialog(program_name="mkbib",
                                 title="About mkbib",
                                 comments="Not much to say, really.")
        dialog.run()
        dialog.destroy()

    def new_window(self, filename=None):
        window = Window(self, filename)
        window.show()

    def open(self, application, files, n_files, hint):
        for giofile in files:
            self.new_window(self, giofile)

    def activate(self, data=None):
        self.new_window()

    def startup(self, data=None):

        action = Gio.SimpleAction(name="new")
        action.connect("activate", lambda a, b: self.activate())
        self.add_action(action)

        action = Gio.SimpleAction(name="about")
        action.connect("activate", self.about_activated)
        self.add_action(action)

        action = Gio.SimpleAction(name="quit")
        action.connect("activate", lambda a, b: self.quit())
        self.add_action(action)

        builder = Gtk.Builder()
        builder.add_from_file("menubar.ui")
        self.set_menubar(builder.get_object("menubar"))
        self.set_app_menu(builder.get_object("app-menu"))


def install_excepthook():
    """ Make sure we exit when an unhandled exception occurs. """
    old_hook = sys.excepthook

    def new_hook(etype, evalue, etb):
        old_hook(etype, evalue, etb)
        while Gtk.main_level():
            Gtk.main_quit()
        sys.exit()
    sys.excepthook = new_hook


if __name__ == "__main__":
    app = mkbib()
    r = app.run(sys.argv)
    sys.exit(r)
