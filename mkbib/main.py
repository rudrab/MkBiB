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
        self.Parser = pybib.parser()
        self.name = ""
        # self.set_icon_from_file(os.path.join(
            # os.path.dirname(__file__), 'mkbib.svg'))
        # New Menu
        action = Gio.SimpleAction(name="save-as")
        action.connect("activate", self.MenuElem.file_save_as_clicked)
        self.add_action(action)

        # Open menu
        action = Gio.SimpleAction(name="open")
        action.connect("activate", self.MenuElem.file_open_clicked)
        self.add_action(action)

        action = Gio.SimpleAction(name="insert")
        action.connect("activate", self.MenuElem.create_textview)
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
                self.npage.attach(self.lfield, xpos, ypos, 2, 1)
                self.npage.attach_next_to(self.all_fields[field], self.lfield,
                                          Gtk.PositionType.RIGHT, 1, 1)
                ypos += 1
                # self.all_fields[field].connect("changed", self.activate_scholar)
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
        # self.bsearch = Gtk.Button("Search Google")
        renderer_text = Gtk.CellRendererText()
        self.bsearch.pack_start(renderer_text, True)
        self.bsearch.set_active(0)
        self.bsearch.add_attribute(renderer_text, "text", 0)
        # self.bsearch.connect("changed", self.search_gschol)
        self.bsearch.connect("changed", self.search_gschol)
        self.bsearch.set_sensitive(False)

        scroll = Gtk.ScrolledWindow()
        scroll.set_hexpand(False)
        scroll.set_vexpand(True)

        grid = Gtk.Grid()
        grid.set_column_spacing(10)
        grid.attach(self.key_combo, 0, 0, 6, 2)
        grid.attach(self.KeyEntry, 8, 0, 4, 2)
        grid.attach(self.notebook, 0, 2, 12, 12)
        grid.attach(scroll, 15, 0, 105, 21)
        grid.attach(self.bcreate, 0, 14,  4, 1)
        grid.attach(self.bsearch, 8, 14,  4, 1)
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
        if (self.KeyEntry.get_text_length() > 0 and len(self.get_combo_data(self.name)) > 0):
            self.bcreate.set_sensitive(True)
        else:
            self.bcreate.set_sensitive(False)

    def activate_scholar(self, widget):
        if (len(self.all_fields["Author"].get_text()) > 0):
            self.bsearch.set_sensitive(True)
        else:
            self.bsearch.set_sensitive(False)

    def search_gschol(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter != None:
            model = combo.get_model()
            api_selected=model[tree_iter][0]
        print(api_selected)
        neworder = [3, 0, 2, 1]
        fields = [self.fields[i] for i in neworder]
        datatup = tuple([self.all_fields[field].get_text() or None
                         for field in fields])
        if api_selected == "Search Google":
            schol = "https://scholar.google.com/scholar?"
            url = schol+lurl.urlencode({"q": datatup[1], "ylo": datatup[3]})
            webbrowser.open(url, new=2)
            print(self.all_fields["Author"].get_text())
        elif api_selected == "Search Crossref":
            authorq = "+".join(datatup[1].split()) #datatup[1].replace(" ","+")
            print(authorq)
            headers = {'Accept': 'application/x-bibtex; charset=utf-8'}
            url = "http://api.crossref.org/works?query.author="
            print(url+authorq)
            jsonget=(urlopen(url+authorq))

            data = (json.loads(jsonget.read().decode()))
            # with open("outp","w") as op:
            # op.write(data)
            for i in range(len(data["message"]["items"][0])):
                url=((data["message"]["items"][i]["URL"]))
                r = requests.get(url, headers=headers)
                r.encoding = "utf-8"
                entry = r.text.strip()
                print(entry)

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


class mkbib(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(self)
        self.connect("startup", self.startup)
        self.connect("activate", self.activate)

    def about_activated(self, action, data=None):
        dialog = Gtk.AboutDialog(program_name="mkbib",
                                 name="About mkbib",
                                 comments="BibTex manager",
                                 version="0.1",
                                 authors=(["Rudra Banerjee"]))
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
#os.path.join(os.path.dirname(__file__), 'menubar.ui')
        builder.add_from_file(os.path.join(os.path.dirname
                                           (__file__), 'menubar.ui'))
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
