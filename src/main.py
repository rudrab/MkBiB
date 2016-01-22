import gi
import menu
import pybib
import view
from gi.repository import Gtk
gi.require_version("Gtk", "3.0")

booklist = [("The Art of Computer Programming", "D.Knuth", "Addison", "1980"),
            ("Feynman Lectures in Physics", "R.P. Feynman", "Addison", "1976")]
columns = ["Index", "Title", "Author", "Publishers" "Year"]


class MyWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="mkBiB")
        self.set_default_size(1000, 200)
        self.set_border_width(10)

        MenuElem = menu.MenuManager()
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.pack_start(MenuElem.menubar, False, False, 0)
        self.add(box)

        parsing = pybib.parser()

        TreeView = view.treeview()
# Generate entry fiels
        key_store = Gtk.ListStore(int, str)
        keys = ["Article", "Book", "Booklet", "Conference", "inBook",
                "inCollection", "inProseedings", "Manual", "MasterThesis",
                "Misc", "PhdThesis", "Proceedings", "TechReport",
                "Unpublished"]
        for key in keys:
            key_store.append([keys.index(key), key])
        key_combo = Gtk.ComboBox.new_with_model_and_entry(key_store)
        key_combo.set_entry_text_column(1)

        KeyEntry = Gtk.Entry()
        KeyEntry.set_placeholder_text("BibtexKey")

#  Generate the Entry fields
        xpos = 0
        minf = 0
        self.notebook = Gtk.Notebook()
        fields = ["Author",  "Year",  "Journal", "Title", "Publisher", "Page",
                  "Address", "Annote", " Booktitle", "Chapter", "Crossred",
                  "Edition", "Editor", "HowPublished", "Institution", "Month",
                  "Note", "Number", "Organization", "Pages", "Publishers",
                  "School", "Series", "Type"]
        Tabs = ["Essential", "Publishers", "Extra", "Extra"]
        for note in range(int(len(fields)/6)):
            ypos = 0
            self.npage = "page"+str(note)
            self.npage = Gtk.Grid()
            self.npage.set_border_width(10)
            maxf = minf+6
            for field in fields[minf:maxf]:
                self.lfield = "L" + field
                self.efield = "E" + field
                self.lfield = Gtk.Label(field)
                self.efield = Gtk.Entry()
                self.efield.set_placeholder_text(field)
                self.npage.attach(self.lfield, xpos, ypos, 2, 1)
                self.npage.attach_next_to(self.efield, self.lfield,
                                          Gtk.PositionType.RIGHT, 1, 1)
                ypos += 1
            self.notebook.append_page(self.npage, Gtk.Label(Tabs[note]))
            minf = maxf

# Now create the treeview
#         booklist = []
#         filename = "mkBiB"
#         # filename = MenuElem.file_open_clicked(filename)
#         hb = Gtk.HeaderBar()
#         hb.set_show_close_button(True)
#         hb.props.title = filename
#         self.set_titlebar(hb)
#         # parsing.parsing_read(filename, booklist)
#         self.bookstore = Gtk.ListStore(int, str, str, str, str)
#         for ref in booklist:
#             self.bookstore.append(list(ref))
#         self.current_filter_language = None
#         self.view = Gtk.TreeView(model=self.bookstore)
#         for i, column_title in enumerate(["Index", "Title", "Author",
#                                           "Publishers", "Year"]):
#             renderer = Gtk.CellRendererText()
#             renderer.set_property("wrap-width", 400)
#             if i > 2:
#                 renderer.set_property("wrap-width", 150)
#             renderer.set_property("wrap-mode", 0)
#             column = Gtk.TreeViewColumn(column_title, renderer, text=i)
#             self.view.append_column(column)

# Create the buttons to get data
        bcreate = Gtk.Button("Create")
        bcreate.connect("clicked", self.get_data)
        bsearch = Gtk.Button("Search Google")
        bsearch.connect("clicked", self.on_button_clicked)

        grid = Gtk.Grid()
        grid.attach(key_combo, 0, 0, 6, 2)
        grid.attach(KeyEntry, 8, 0, 4, 2)
        grid.attach(TreeView.view, 30, 0, 25, 21)
        grid.attach(self.notebook, 0, 2, 12, 12)
        grid.attach(bcreate, 0, 14,  4, 1)
        grid.attach(bsearch, 8, 14,  4, 1)
        box.pack_start(grid, False, False, 0)

    def on_button_clicked(self, widget):
        print("Hello World")

    def get_data(self, widget):
        print(self.KeyEntry.get_text())
        dAu = self.EAuthor.get_text()
        dJo = self.EJournal.get_text()
        dYe = self.EYear.get_text()
        print(dAu)
        print(dJo)
        print(dYe)


win = MyWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
