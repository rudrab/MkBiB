#!/usr/bin/python3

import gi
import sys
import menu
import view
import pybib
import urllib.parse as lurl
import webbrowser
import os
import requests
from urllib.request import urlopen
import json
from pprint import pprint
import io
from gi.repository import GdkPixbuf
from gi.repository import Gtk, Gio  # , GLib, Gdk
gi.require_version("Gtk", "3.0")


class Window(Gtk.ApplicationWindow):
    def __init__(self, application, giofile=None):
        Gtk.ApplicationWindow.__init__(self,
                                       application=application,
                                       default_width=1000,
                                       default_height=200,
                                       title="mkbib")

        # Import other files
        self.TreeView = view.treeview()
        self.MenuElem = menu.MenuManager()
        self.Parser = pybib.parser()

        #
        # Create HeaderBar and manu
        headerbar = Gtk.HeaderBar()
        self.set_titlebar(headerbar)
        headerbar.set_show_close_button(True)
        # menuicon = Gtk.Image.new_from_icon_name("mkbib-symbolic", 32);
        # Gtk.HeaderBar.pack_start(headerbar,menuicon);
        headerbar.set_title("MkBiB")

        icontheme = Gtk.IconTheme.get_default()
        self.icon = icontheme.load_icon("mkbib",64,0)

        # Menu using Gio
        h_grid = Gtk.Grid()
        FileButton = Gtk.MenuButton()
        EditButton = Gtk.MenuButton(None,image=Gtk.Image(icon_name="list-add-symbolic"))
        # FileButton = Gtk.MenuButton()
        # FileButton.set_size_request(80, 35)
        # EditButton.set_size_request(40, 35)
        FileButton.props.label="File"
        # EditButton.props.icon="Edit"
        filemenu = Gio.Menu()
        editmenu = Gio.Menu()
        filemenu.append("Open", "win.open")
        filemenu.append("Save As", "win.save-as")
        filemenu.append("Save", "app.save")
        filemenu.append("Quit", "app.quit")
        # menumodel.append_submenu("File", filemenu)
        editmenu.append("Edit", "win.edit")
        # menumodel.append("Help", "win.about")
        h_grid.attach(FileButton, 0, 0, 3, 1)
        h_grid.attach(EditButton, 3, 0, 1, 1)
        FileButton.set_menu_model(filemenu)
        EditButton.set_menu_model(editmenu)
        headerbar.pack_start(h_grid)
        # headerbar.pack_start(EditButton)

        about_action = Gio.SimpleAction.new("about", None)
        about_action.connect("activate", Window.about_activated)
        self.add_action(about_action)

        # accelgroup=Gtk.AccelGroup()
        # self.add_accel_group(accelgroup)

        # Menu (Stable)
        action = Gio.SimpleAction(name="save-as")
        action.connect("activate", self.MenuElem.file_save_as_clicked)
        self.add_action(action)

        # Open menu
        open_action = Gio.SimpleAction(name="open")
        open_action.connect("activate", self.MenuElem.file_open_clicked)
        self.add_action(open_action)

        action = Gio.SimpleAction(name="edit")
        action.connect("activate", self.MenuElem.create_textview)
        self.add_action(action)

        # Add accel
        # accel_group = Gtk.AccelGroup()
        # self.add_accel_group(accel_group)
        # open_action.add_accelerator("activate", accel_group, ord("O"))

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
        self.key_combo.connect("changed", self.get_combo_data)
        self.key_combo.connect("changed", self.activate_button)

        # BibTeX Key
        self.KeyEntry = Gtk.Entry()
        self.KeyEntry.set_placeholder_text("BibtexKey")
        self.KeyEntry.connect("changed", self.activate_button)

        #  Generate the  Fields
        self.notebook = Gtk.Notebook()
        xpos = 0
        minf = 0
        self.all_fields = dict()
        self.fields = ["Author",  "Year",  "Journal", "Title", "Publisher",
                       "Page", "Address", "Annote", " Booktitle", "Chapter",
                       "Crossred", "Edition", "Editor", "HowPublished",
                       "Institution", "Month", "Note", "Number",
                       "Organization", "Pages", "School",
                       "Series", "Type", "Volume"]
        Tabs = ["Essential", "Publishers", "Extra I", "Extra II"]
        for note in range(int(len(self.fields)/6)):
            ypos = 0
            self.npage = "page"+str(note)
            self.npage = Gtk.Grid()
            self.npage.set_border_width(10)
            maxf = minf+6
            for field in self.fields[minf:maxf]:
                # print(type(field))
                # print(field)
                self.lfield = "L" + field
                self.lfield = Gtk.Label(field)
                self.all_fields[field] = Gtk.Entry()
                self.all_fields[field].set_placeholder_text(field)
                self.npage.attach(self.lfield, xpos, ypos, 1, 1)
                self.lfield.set_yalign(0)
                self.npage.attach_next_to(self.all_fields[field], self.lfield,
                                          Gtk.PositionType.RIGHT, 14, 1)
                ypos += 1
                # self.all_fields[field].connect("changed",
                #   self.activate_scholar)
            self.notebook.append_page(self.npage, Gtk.Label(Tabs[note]))
            minf = maxf

        self.all_fields["Author"].connect("changed", self.activate_scholar)

        # Create button to get data from manual entry
        self.bcreate = Gtk.Button("Create")
        self.bcreate.set_sensitive(False)
        self.bcreate.connect("clicked", self.get_data)

        # Create the buttons to get data
        # Google/Crossref data fetch
        api_store = Gtk.ListStore(str)
        apis = ["==Select search engine==", "Search Google", "Search Crossref"]
        for api in apis:
            api_store.append([api])
        self.bsearch = Gtk.ComboBox.new_with_model(api_store)
        renderer_text = Gtk.CellRendererText()
        self.bsearch.pack_start(renderer_text, True)
        self.bsearch.set_active(0)
        self.bsearch.add_attribute(renderer_text, "text", 0)
        self.bsearch.connect("changed", self.search_gschol)
        self.bsearch.set_sensitive(False)

        scroll = Gtk.ScrolledWindow()
        scroll.set_hexpand(False)
        scroll.set_vexpand(True)

        grid = Gtk.Grid()
        grid.set_column_spacing(10)
        grid.attach(self.key_combo, 0, 0, 4, 2)
        grid.attach(self.KeyEntry, 4, 0, 4, 2)
        grid.attach(self.notebook, 0, 2, 8, 12)
        grid.attach(scroll, 15, 0, 105, 15)
        grid.attach(self.bcreate, 0, 14,  4, 1)
        grid.attach(self.bsearch, 4, 14,  4, 1)
        box.pack_start(grid, False, False, 0)
        scroll.add(self.TreeView.view)
        self.show_all()

    def get_combo_data(self, name):
        tree_iter = self.key_combo.get_active_iter()
        if tree_iter is not None:
            model = self.key_combo.get_model()
            row_id, self.name = model[tree_iter][:2]
        else:
            entry = self.key_combo.get_child()
            self.name = entry.get_text()
        return(self.name)

    def activate_button(self, widget):
        if (self.KeyEntry.get_text_length() > 0 and
                len(self.get_combo_data(self.name)) > 0):
            self.bcreate.set_sensitive(True)
        else:
            self.bcreate.set_sensitive(False)

    def activate_scholar(self, widget):
        if (len(self.all_fields["Author"].get_text()) > 0):
            self.bsearch.set_sensitive(True)
        else:
            self.bsearch.set_sensitive(False)

    def search_gschol(self, combo):
        model = combo.get_model()
        api_selected = combo.get_active()
        if api_selected == 1:
            self.search_gs()
        elif api_selected == 2:
            self.search_cr()

    def search_gs(self):
        neworder = [3, 0, 2, 1]
        fields = [self.fields[i] for i in neworder]
        datatup = tuple([self.all_fields[field].get_text() or None
                         for field in fields])
        schol = "https://scholar.google.com/scholar?"
        url = schol+lurl.urlencode({"q": datatup[1], "ylo": datatup[3]})
        webbrowser.open(url, new=2)
        print(self.all_fields["Author"].get_text())

    def search_cr(self):
        neworder = [3, 0, 2, 1]
        fields = [self.fields[i] for i in neworder]
        datatup = tuple([self.all_fields[field].get_text() or None
                        for field in fields])
        authorq = "+".join(datatup[1].split())
        # print(authorq)
        headers = {'Accept': 'application/x-bibtex; charset=utf-8'}
        url = "http://api.crossref.org/works?query.author="
        # print(url+authorq+"&rows=100")
        jsonget = (urlopen(url+authorq+"&rows=100"))
        data = (json.loads(jsonget.read().decode()))

        # First, open a window to dispaly data
        self.crrefwin = Gtk.Window()
        # Gtk.Window.set_decorated(self.crrefwin, False)
        self.crrefwin.set_default_size(950, 350)
        grid = Gtk.Grid()
        cr_header = Gtk.HeaderBar()
        self.crrefwin.set_titlebar(cr_header)
        cr_header.set_title("CrossRef Search: "+str(datatup[1]))
        cr_header.set_show_close_button(True)
        spinner = Gtk.Spinner()
        cr_header.pack_end(spinner)
        spinner.start()

        self.cr_liststore = Gtk.ListStore(int, str, str, str, str)
        self.treeview = Gtk.TreeView(model=self.cr_liststore)
        for i, column_title in enumerate(["Index", "Title", "Author",
                                          "Journal", "Year"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.treeview.append_column(column)
            renderer.set_property("wrap-width", 300)
            renderer.set_property("wrap-mode", 0)

        self.get_selection = self.treeview.get_selection()
        self.get_selection.set_mode(Gtk.SelectionMode.MULTIPLE)
        self.scrolw = Gtk.ScrolledWindow()
        self.scrolw.set_hexpand(True)
        self.scrolw.set_vexpand(True)
        self.select_button = Gtk.Button.new_with_label("Export")
        self.select_button.connect("clicked", self.extract_data_from_cr)
        grid.attach(self.scrolw, 0,  1, 10, 10)
        cr_header.pack_start(self.select_button)
        self.scrolw.add(self.treeview)
        self.crrefwin.add(grid)
        self.crrefwin.show_all()

        self.cr_entry = []
        for i in range(len(data["message"]["items"][0])):
            # Too fast..wait a bit to view
            while Gtk.events_pending():
                Gtk.main_iteration_do(False)
            url = ((data["message"]["items"][i]["URL"]))
            r = requests.get(url, headers=headers)
            r.encoding = "utf-8"
            self.cr_entry.append(r.text.strip())
            api_tups = list(self.Parser.parsing_read
                            (io.StringIO(r.text.strip())))
            api_tups[1] = i
            self.cr_liststore.append((api_tups[1:6]))

        spinner.stop()
        self.bsearch.set_active(0)

    def extract_data_from_cr(self, select_button):
        (model, pathlist) = self.get_selection.get_selected_rows()
        for path in pathlist :
            tree_iter = model.get_iter(path)
            value = model.get_value(tree_iter,0)
            print(type(self.cr_entry[value]))
            text = io.StringIO(self.cr_entry[value])
            del self.Parser.booklist[:]
            self.Parser.parsing_read(text)
            self.TreeView.viewer(self.Parser.booklist)
        self.crrefwin.destroy()


    def get_data(self, datalist):
        neworder = [3, 0, 2, 1, 4, 5, 6, 7, 8, 9, 10, 11, 12,
                    13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
        fields = [self.fields[i] for i in neworder]
        datatup = tuple([self.name] + [self.KeyEntry.get_text()] +
                        [self.all_fields[field].get_text() or None
                         for field in fields])
        # print(datatup)
        self.Parser.booklist.clear()
        self.Parser.booklist.append(datatup)
        self.TreeView.viewer(self.Parser.booklist)
        # reset Entries to initial value
        self.KeyEntry.set_text("")
        [self.all_fields[field].set_text("") for field in fields]

    def about_activated(action, data=None):
        copyright = "Copyright \u00a9 2016- - Rudra Banerjee"
        comments = "BiBTeX Manager"
        dialog = Gtk.AboutDialog(program_name="MkBiB",
                                 name="About MkBiB",
                                 comments=comments,
                                 version="0.1",
                                 copyright = copyright,
                                 license_type=Gtk.License.GPL_3_0,
                                 authors=(["Rudra Banerjee"]))
        # dialog.set_transient(Window)
        dialog.set_logo(GdkPixbuf.Pixbuf.new_from_file_at_size(
            "/home/rudra/Devel/Icons/shadow/scalable/apps/mkbib.svg", 128,128))
        dialog.run()
        dialog.destroy()


class mkbib(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(self)
        self.connect("startup", self.startup)
        self.connect("activate", self.activate)

    # def about_activated(self, action, data=None):
        # dialog = Gtk.AboutDialog(program_name="mkbib",
                                 # name="About mkbib",
                                 # comments="BibTex manager",
                                 # version="0.1",
                                 # authors=(["Rudra Banerjee"]))
        # dialog.run()
        # dialog.destroy()

    def new_window(self, filename=None):
        window = Window(self, filename)
        window.show()

#     def open(self, application, files, n_files, hint):
#         for giofile in files:
#             self.new_window(self, giofile)

    def activate(self, data=None):
        self.new_window()

    def startup(self, data=None):

        # For app-menu
        # I would try to merge them later
        action = Gio.SimpleAction(name="new")
        action.connect("activate", lambda a, b: self.activate())
        self.add_action(action)


        action = Gio.SimpleAction(name="about")
        action.connect("activate", Window.about_activated)
        self.add_action(action)

        action = Gio.SimpleAction(name="quit")
        action.connect("activate", lambda a, b: self.quit())
        self.add_action(action)

        builder = Gtk.Builder()
        builder.add_from_file(os.path.join(os.path.dirname
                                           (__file__), '../data/menubar.ui'))

        # self.set_menubar(builder.get_object("menubar"))
        self.set_app_menu(builder.get_object("app-menu"))

        self.set_accels_for_action("win.about",["<Ctrl>h"])
        self.set_accels_for_action("win.open",["<Ctrl>o"])
        self.set_accels_for_action("win.edit",["<Ctrl>I"])
        self.set_accels_for_action("win.save",["<Ctrl>s"])

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
