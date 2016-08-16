#!/usr/bin/python3
import gi
import sys
import Mkbib.menu as menu
import math
import Mkbib.view as view
import Mkbib.pybib as pybib
import Mkbib.dialogue as dialogue
import Mkbib.filemanager as filemanager
import Mkbib.cell as cell
import Mkbib.getdata as getdata
import urllib.parse as lurl
import webbrowser
import os
import requests
from urllib.request import urlopen
import json
from pprint import pprint
import io
import time
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, Gdk


class Window(Gtk.ApplicationWindow):
    def __init__(self, application, giofile=None):
        Gtk.ApplicationWindow.__init__(self,
                                       application=application,
                                       default_width=1000,
                                       default_height=200,
                                       border_width=5)

        # Import other files
        self.TreeView = view.treeview()
        self.MenuElem = menu.MenuManager()
        self.Parser = pybib.parser()
        self.Dialog = dialogue.FileDialog()
        self.Messages = dialogue.MessageDialog()
        self.Files = filemanager.file_manager()
        self.Datas = getdata.data()
        self.Cell  = cell.cell_renderer()
        #
        # Create HeaderBar and manu
        self.headerbar = Gtk.HeaderBar()
        self.set_titlebar(self.headerbar)
        self.headerbar.set_show_close_button(True)
        # menuicon = Gtk.Image.new_from_icon_name("mkbib-symbolic", 32);
        # Gtk.HeaderBar.pack_start(headerbar,menuicon);

        # global main_header
        self.main_header = "MkBiB"
        self.headerbar.set_title(self.main_header)

        icontheme = Gtk.IconTheme.get_default()
        self.icon = icontheme.load_icon("mkbib", 64, 0)

        # Menu using Gio
        h_grid = Gtk.Grid()
        FileButton = Gtk.MenuButton()
        EditButton = Gtk.MenuButton(
            None, image=Gtk.Image(icon_name="list-add-symbolic"))
        FileButton.props.label = "File"
        filemenu = Gio.Menu()
        editmenu = Gio.Menu()
        filemenu.append("Open", "win.open")
        filemenu.append("Save As", "win.save-as")
        filemenu.append("Save", "app.save")
        filemenu.append("Quit", "app.quit")
        # menumodel.append_submenu("File", filemenu)
        editmenu.append("Copy BiBTeX", "win.edit")
        # menumodel.append("Help", "win.about")
        h_grid.attach(FileButton, 0, 0, 3, 1)
        h_grid.attach(EditButton, 3, 0, 1, 1)
        FileButton.set_menu_model(filemenu)
        EditButton.set_menu_model(editmenu)
        self.headerbar.pack_start(h_grid)
        # headerbar.pack_start(EditButton)

        about_action = Gio.SimpleAction.new("about", None)
        about_action.connect("activate", self.Messages.about_activated)
        self.add_action(about_action)

        # accelgroup=Gtk.AccelGroup()
        # self.add_accel_group(accelgroup)

        # Menu (Stable)
        action = Gio.SimpleAction(name="save-as")
        action.connect("activate", self.file_save_as_clicked)
        self.add_action(action)

        # Open menu
        open_action = Gio.SimpleAction(name="open")
        open_action.connect("activate", self.file_open_clicked)
        self.add_action(open_action)

        action = Gio.SimpleAction(name="edit")
        action.connect("activate", self.MenuElem.create_textview)
        self.add_action(action)

        # Statusbar
        self.Files.chk_rootdir()
        self.status = Gtk.Statusbar()
        self.context = self.status.get_context_id("example")
        self.status.push(self.context, self.Files.root_status)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
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
                       "Page", "Address", "Annote", "Booktitle", "Chapter",
                       "Crossred", "Edition", "Editor", "HowPublished",
                       "Institution", "Month", "Note", "Number",
                       "Organization", "Pages", "School",
                       "Series", "Type", "Volume", "DOI", "File"]
        # self.fields = self.Parser.entries
        # self.fields = [item.capitalize() for item in self.fields]
        Tabs = ["Essential", "Publishers", "Extra I", "Extra II", "Extra III"]
        for note in range(math.ceil(len(self.fields)/6)):
            ypos = 0
            self.npage = "page"+str(note)
            self.npage = Gtk.Grid()
            self.npage.set_border_width(10)
            maxf = minf+6
            for field in self.fields[minf:maxf]:
                self.lfield = "L" + field
                self.lfield = Gtk.Label(field)
                self.lfield.set_xalign(0)
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
            pdf_load_button = Gtk.Button(image=Gtk.Image(
                icon_name="list-add-symbolic"))
            pdf_load_button.connect("clicked", self.file_attach_cb)
        self.npage.attach_next_to(pdf_load_button, self.all_fields["File"],
                                  Gtk.PositionType.RIGHT, 2, 1)

        # Set tooltip for searchable entries
        self.all_fields["Author"].set_tooltip_text("Search with Google or CrossRef")
        self.all_fields["Year"].set_tooltip_text("Refine Author search with Google")
        self.all_fields["Title"].set_tooltip_text("Search by Title")
        self.all_fields["DOI"].set_tooltip_text("Search DOI")

        self.all_fields["Author"].connect("changed", self.activate_scholar)
        self.all_fields["DOI"].connect("changed", self.activate_scholar)
        self.all_fields["Title"].connect("changed", self.activate_scholar)
        self.all_fields["File"].connect("changed", self.activate_scholar)

        # Create button to get data from manual entry
        self.bcreate = Gtk.Button("Create Manually")
        self.bcreate.set_sensitive(False)
        self.bcreate.connect("clicked", self.get_data)

        # Create the buttons to get data
        # Google/Crossref data fetch
        api_store = Gtk.ListStore(str)
        apis = ["Search", "Search Google", "Search Crossref",
                "Search DOI", "Search by Title", "From PDF"]
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

        # self.overlay = Gtk.Overlay()
        # self.overlay.add(scroll)
        # self.box = Gtk.Box()
        # self.box.override_background_color(Gtk.StateType.NORMAL,
                                           # Gdk.RGBA(.5,.5,.5, 1))
        # self.box.pack_start(self.status, True, True, 0)
        # self.box.set_valign(Gtk.Align.END)
        # self.overlay.add_overlay(self.box)
        grid = Gtk.Grid()
        grid.set_column_spacing(10)
        grid.attach(self.key_combo, 0, 0, 1, 1)
        grid.attach(self.KeyEntry, 1, 0, 1, 1)
        # grid.attach(self.status, 0, 3, 20, 1)
        grid.attach(self.notebook, 0, 1, 2, 1)
        grid.attach(scroll, 2, 0, 105, 4)
        grid.attach(self.bcreate, 0, 2,  1, 1)
        grid.attach(self.bsearch, 1, 2,  1, 1)
        box.pack_start(grid, False, False, 0)
        scroll.add(self.TreeView.view)
        # self.overlay.show_all()
        self.show_all()

    def file_open_clicked(self, name, action):
        self.Dialog.FileChooser(["Open Existing BiBTeX File",
                                 "BiBTeX File", "*.bib"],
                                Gtk.FileChooserAction.OPEN, Gtk.STOCK_OPEN)
        if self.Dialog.response == Gtk.ResponseType.OK:
            filename = self.Dialog.dialog.get_filename()
            self.Dialog.dialog.destroy()
            del self.TreeView.full_list[:]
            self.Parser.booklist = []
            self.TreeView.bookstore.clear()
            self.TreeView.indxcount = 0
            with open(filename, "r") as fname:
                self.Parser.parsing_read(fname)
                self.Files.chk_subdir(os.path.splitext(os.path.basename(filename))[0])
                self.status.push(self.context, self.Files.base_status)
                # self.status.connect("text-pushed", self.hide_statusbar, "example")
                self.headerbar.set_title(self.main_header+" : "+filename)
            self.TreeView.viewer(self.Parser.booklist)
        elif self.Dialog.response == Gtk.ResponseType.CANCEL:
            self.Dialog.dialog.destroy()

    # def hide_statusbar(self):
        # print("pushed")
        # time.sleep(1)
        # self.box.hide()

    def file_save_as_clicked(self, name, action):
        self.Dialog.FileChooser(["Save as an existing file",
                                 "BiBTeX File", "*.bib"],
                                 Gtk.FileChooserAction.SAVE, Gtk.STOCK_SAVE)
        if self.Dialog.response == Gtk.ResponseType.OK:
            filename = self.Dialog.dialog.get_filename()
            print(filename)
            self.Parser.parsing_write(filename)
            self.Dialog.dialog.destroy()
        elif self.Dialog.response == Gtk.ResponseType.CANCEL:
            self.Dialog.dialog.destroy()

    def on_menu_file_quit(self, widget):
        Gtk.main_quit()

    def file_attach_cb(self, name):
        self.Dialog.FileChooser(["Open Pdf file", "PDF File", "*.pdf"],
                                Gtk.FileChooserAction.OPEN, Gtk.STOCK_OPEN)
        if self.Dialog.response == Gtk.ResponseType.OK:
            self.path = self.Dialog.dialog.get_filename()
            self.all_fields["File"].set_text(self.path)
            self.Dialog.dialog.destroy()
        elif self.Dialog.response == Gtk.ResponseType.CANCEL:
            self.Dialog.dialog.destroy()


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
        if ((len(self.all_fields["Author"].get_text()) > 0) or
            (len(self.all_fields["DOI"].get_text()) > 0)    or
            (len(self.all_fields["Title"].get_text()) > 0)  or
            (len(self.all_fields["File"].get_text()) > 0)
            ):
            self.bsearch.set_sensitive(True)
        else:
            self.bsearch.set_sensitive(False)

    def search_gschol(self, combo):
        model = combo.get_model()
        api_selected = combo.get_active()
        # Search Google Scholar
        if api_selected == 1:
            neworder = [3, 0, 2, 1]
            fields = [self.fields[i] for i in neworder]
            datatup = tuple([self.all_fields[field].get_text() or None
                         for field in fields])
            self.Datas.search_gs(datatup[1], datatup[3])
        # Search CrossRef
        elif api_selected == 2:
            neworder = [3, 0, 2, 1]
            fields = [self.fields[i] for i in neworder]
            datatup = tuple([self.all_fields[field].get_text() or None
                             for field in fields])
            authorq = "+".join(datatup[1].split())
            self.Datas.search_cr(authorq)
        # Search DOI
        elif api_selected ==3:
            self.Cell.search_doi(self.all_fields["DOI"].get_text())
        # Search Title
        elif api_selected == 4:
            title = self.all_fields["Title"].get_text()
            self.Datas.gs_advanced(title)
        elif api_selected == 5:
            filename = self.all_fields["File"].get_text()
            self.Datas.exif_pdf(filename)
        # Reset fields
        for i in self.all_fields:
            self.all_fields[i].set_text("")
        self.bsearch.set_active(0)

    def get_data(self, datalist):
        neworder = [3, 0, 2, 1, 4, 5, 6, 7, 8, 9, 10, 11, 12,
                    13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
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

        self.Messages = dialogue.MessageDialog()
        self.Files = filemanager.file_manager()
    def new_window(self, filename=None):
        window = Window(self, filename)
        window.show()


    def activate(self, data=None):
        self.new_window()

    def startup(self, data=None):

        # For app-menu
        # I would try to merge them later
        action = Gio.SimpleAction(name="new")
        action.connect("activate", lambda a, b: self.activate())
        self.add_action(action)

        action = Gio.SimpleAction(name="about")
        action.connect("activate", self.Messages.about_activated)
        self.add_action(action)

        action = Gio.SimpleAction(name="quit")
        action.connect("activate", lambda a, b: self.quit())
        self.add_action(action)

        builder = Gtk.Builder()
        builder.add_from_file(os.path.join(os.path.dirname
                                           (__file__), '../../../../share/mkbib/ui/menubar.ui'))

        self.set_app_menu(builder.get_object("app-menu"))

        self.set_accels_for_action("win.about", ["<Primary>h"])
        self.set_accels_for_action("win.open", ["<Primary>o"])
        self.set_accels_for_action("win.edit", ["<Primary>I"])
        self.set_accels_for_action("win.save", ["<Primary>s"])


def install_excepthook():
    """ Make sure we exit when an unhandled exception occurs. """
    old_hook = sys.excepthook

    def new_hook(etype, evalue, etb):
        old_hook(etype, evalue, etb)
        while Gtk.main_level():
            Gtk.main_quit()
        sys.exit()
    sys.excepthook = new_hook

def main(version=""):
    app = mkbib()
    r = app.run(sys.argv)
    sys.exit(r)

if __name__ == "__main__":
    main()
