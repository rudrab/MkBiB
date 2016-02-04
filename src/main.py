import gi
import menu
# import pybib
import view
from gi.repository import Gtk
gi.require_version("Gtk", "3.0")


class MyWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="mkBiB")
        self.set_default_size(1000, 200)
        self.set_border_width(10)

        MenuElem = menu.MenuManager()
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.pack_start(MenuElem.menubar, False, False, 0)
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

        # Get headerbar
        # hb = Gtk.HeaderBar()
        # hb.props.title = MenuElem.file_open_clicked(filename)

        # Create the buttons to get data
        bcreate = Gtk.Button("Create")
        bcreate.connect("clicked", self.get_data)
        bsearch = Gtk.Button("Search Google")
        bsearch.connect("clicked", self.on_button_clicked)

        scroll = Gtk.ScrolledWindow()
        # scroll.set_border_width(10)
        scroll.set_hexpand(False)
        scroll.set_vexpand(True)
        # scroll.connect("size-allocate", self.on_resize, scroll, self.Treeview.view)

        grid = Gtk.Grid()
        grid.set_column_spacing(20)
        grid.attach(self.key_combo, 0, 0, 6, 2)
        grid.attach(self.KeyEntry, 8, 0, 4, 2)
        grid.attach(self.notebook, 0, 2, 12, 12)
        grid.attach(scroll, 15, 0, 57, 21)
        grid.attach(bcreate, 0, 14,  4, 1)
        grid.attach(bsearch, 8, 14,  4, 1)
        box.pack_start(grid, False, False, 0)
        scroll.add(self.TreeView.view)

    def on_button_clicked(self, widget):
        print("Hello World")

    def get_data(self, widget):
        # First, get Type
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
        datadict = []
        datadict.append(name)
        datadict.append(self.KeyEntry.get_text())
        datatup = tuple([name] + [self.KeyEntry.get_text()] +
                        [self.all_fields[field].get_text() or None
                         for field in fields])
        datalist.append(datatup)
        self.TreeView.viewer(datalist)

win = MyWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
