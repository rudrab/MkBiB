import Mkbib.view as view
import Mkbib.pybib as pybib
import Mkbib.dialogue as dialogue
import Mkbib.filemanager as filemanager
import Mkbib.menu as menu
import requests
import urllib.parse as lurl
from urllib.request import urlopen
import webbrowser
import json
from pprint import pprint
import io
import gi
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase
from _thread import start_new_thread, allocate_lock
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, GLib
import pyexifinfo  as pexif
class data():
    def __init__(self):
        self.TreeView = view.treeview()
        self.Parser = pybib.parser()
        self.Dialog = dialogue.FileDialog()
        self.Messages = dialogue.MessageDialog()
        self.Files = filemanager.file_manager()
        self.Menu = menu.MenuManager()

    def search_gs(self, auth, year):
        schol = "https://scholar.google.com/scholar?"
        url = schol+lurl.urlencode({"q": auth, "ylo": year})
        webbrowser.open(url, new=2)

    def search_cr(self, authorq):
        url = "http://api.crossref.org/works?query.author="
        self.jsonget = (urlopen(url+authorq+"&rows=50"))
        self.crrefwin = Gtk.Window(border_width=5)
        self.crrefwin.set_default_size(950, 350)
        grid = Gtk.Grid()
        cr_header = Gtk.HeaderBar()
        self.crrefwin.set_titlebar(cr_header)
        cr_header.set_title("CrossRef Search: "+str(authorq))
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
            if i > 2:
                renderer.set_property("wrap-width", 150)
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
        for i in range(4):
            start_new_thread(self.populate_crwin,("thread"+str(i),))
        spinner.stop()

    def populate_crwin(self, threadName):
        print(threadName)
        headers = {'Accept': 'application/x-bibtex; charset=utf-8'}
        data = (json.loads(self.jsonget.read().decode()))
        self.cr_entry = []
        for i in range(len(data["message"]["items"][0])):
            url = ((data["message"]["items"][i]["URL"]))
            r = requests.get(url, headers=headers)
            r.encoding = "utf-8"
            self.cr_entry.append(r.text.strip())
            api_tups = list(self.Parser.parsing_read
                            (io.StringIO(r.text.strip())))
            api_tups[1] = i
            self.cr_liststore.append((api_tups[1:6]))

    def extract_data_from_cr(self, select_button):
        (model, pathlist) = self.get_selection.get_selected_rows()
        for path in pathlist:
            tree_iter = model.get_iter(path)
            value = model.get_value(tree_iter, 0)
            text = io.StringIO(self.cr_entry[value])
            del self.Parser.booklist[:]
            self.Parser.parsing_read(text)
            biblst= [list(elem) for elem in self.Parser.booklist]
            biblst[0].insert(0, self.TreeView.row_num)
            # self.TreeView.bookstore.append(biblst[0])
            self.TreeView.viewer(self.Parser.booklist)
        self.crrefwin.destroy()
        text.close()

    def gs_advanced(self, title):
        google_as = "https://www.google.com/search?"
        url = google_as+lurl.urlencode({"as_q":"", "as_epq": title})
        webbrowser.open(url, new=2)

    def exif_pdf(self, filename):
        fields = ["Author", "Year",  "Journal", "Title", "Publisher",
                       "Page", "Address", "Annote", "Booktitle", "Chapter",
                       "Crossred", "Edition", "Editor", "HowPublished",
                       "Institution", "Month", "Note", "Number",
                       "Organization", "Pages", "School",
                       "Series", "Type", "Volume", "Doi", "File"]
        op=pexif.get_json(filename)
        new_op = {
            field: str(value) for field in fields
            for key, value in op[0].items() if field.lower() in key.lower()
        }
        id_auth=new_op["Author"].split()[-1]
        id_tit = (new_op["Title"].split()[:2])
        id_tit.append(id_auth)
        id_val = "_".join(id_tit)
        new_op["ID"] = str(id_val)
        new_op["ENTRYTYPE"] = "article"
        op[0] = new_op
        db = BibDatabase()
        db.entries = op
        writer =  BibTexWriter()
        pdf_buff = (writer.write(db))
        self.create_textview(pdf_buff)

    def create_textview(self, text):
        popup = Gtk.Window(border_width=5)
        popup.set_title("Add a complete bibtex entry")
        popup.set_default_size(350, 350)
        grid = Gtk.Grid()
        scrolw = Gtk.ScrolledWindow()
        scrolw.set_hexpand(True)
        scrolw.set_vexpand(True)
        button = Gtk.Button("Create")
        tview = Gtk.TextView()
        tview.set_wrap_mode(Gtk.WrapMode.WORD)

        # Get the buffer
        txtbuffer = tview.get_buffer()
        txtbuffer.set_text(text)
        scrolw.add(tview)
        grid.attach(scrolw, 0,  0, 10, 10)
        grid.attach(button, 0, 11, 10,  1)
        button.connect("clicked", self.Menu.create_from_buffer,
                       txtbuffer, popup)
        popup.add(grid)
        popup.show_all()


