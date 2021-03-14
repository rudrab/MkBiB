###########################################
# view.py
# Author: Rudra Banerjee
# Last Update: 01/09/2016
#
# The right hand side of the viewer
# License: GPLv3
###########################################
import gi

gi.require_version("Gtk", "3.0")  #isort:skip
import os

import Mkbib
import Mkbib.cell as cell
import Mkbib.dialogue as dialogue
import Mkbib.preferences as preferences
from gi.repository import GdkPixbuf, Gtk


class treeview():
  row_num = 0
  full_list = []
  booklist = []
  indxcount = 0
  bookstore = Gtk.ListStore(int, str, str, str, str, str, str, str, str, str,
                            str, str, str, str, str, str, str, str, str, str,
                            str, str, str, str, str, str, str, str, str, str,
                            str)
  viewstore = Gtk.ListStore(str, str)

  # Need to be aligned properly
  # Type and value doesnot match
  neworder = [
      3, 0, 2, 1, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
      21, 22, 23, 26, 24, 25, 27
  ]
  entries = [Mkbib.fields[i] for i in neworder]
  entries.insert(0, "ID")
  entries.insert(0, "Type")

  #  entries = Mkbib.fields #["Title", "Author", "Journal", "Year", "Publisher",
  #"Page", "Address", "Annote", "Booktitle", "Chapter", "Crossred",
  #"Edition", "Editor", "Howpublished", "Institution", "Month",
  #"Note", "Number", "Organization", "Pages", "School", "Series",
  #"Type", "Url", "Volume", "DOI", "File"]

  def __init__(self):
    self.indx = 0
    self.cell = cell.cell_renderer()
    self.view = Gtk.TreeView(model=self.bookstore)
    self.Dialog = dialogue.FileDialog()
    self.Files = preferences.file_manager()
    self.Message = dialogue.MessageDialog()
    # Put all crc edit inside this block

    liststore_props = Gtk.ListStore(str)
    props = ["Open", "Edit", "Open Document", "Delete"]
    for item in props:
      liststore_props.append([item])
    renderer_combo = Gtk.CellRendererCombo()
    renderer_combo.set_property("editable", True)
    renderer_combo.set_property("model", liststore_props)
    renderer_combo.set_property("text-column", 0)
    renderer_combo.set_property("has-entry", False)
    renderer_combo.connect("edited", self.on_combo_changed)
    column_combo = Gtk.TreeViewColumn("Index", renderer_combo, text=0)
    arrow_renderer = Gtk.CellRendererPixbuf()
    arrow_renderer.set_property("icon-name", "list-add-symbolic")
    column_combo.pack_start(arrow_renderer, False)
    self.view.append_column(column_combo)
    # column_combo.connect("clicked", self.on_combo_changed)

    # This is crc block

    for i, column_title in enumerate(
        #  ["Type", "Key", "Title", "Author", "Journal", "Year"]):
        ["Type", "Key"] + Mkbib.fields[:4]):
      renderer = Gtk.CellRendererText()
      renderer.set_property("wrap-width", 100)
      if i > 1:
        renderer.set_property("wrap-width", 300)
      renderer.set_property("wrap-mode", 0)
      column = Gtk.TreeViewColumn(column_title, renderer, text=i + 1)
      self.view.append_column(column)
      for cid in range(0, 6):
        column.set_sort_column_id(cid)
    # self.view.connect("row-activated", self.row_activated)

  def on_combo_changed(self, widget, path, text):
    # self.bookstore[path][7] = text
    (model, path) = self.view.get_selection().get_selected_rows()
    tree_iter = model.get_iter(path)
    combo_indx = model.get_value(tree_iter, 0)
    self.cell.row_activated(self.view, str(combo_indx), 0)
    if text == "Open":
      self.cell.search_doi(self.cell.doi)
    elif text == "Edit":
      self.edit_clicked(self.view, str(combo_indx), 0)
    elif text == "Open Document":
      self.row_activated(self.view, str(combo_indx), 0)
      if self.cell.doc:
        self.Files.open_file(os.path.basename(self.cell.doc))
      else:
        self.Message.on_error_clicked("No File attached",
                                      "Attach a file first")
    elif text == "Delete":
      (model, iter) = self.view.get_selection().get_selected()
      self.bookstore.remove(iter)
    else:
      print("Wait")

  def viewer(self, booklist, act=-1):
    for ref in booklist:
      lref = list(ref)
      # print(act)
      if act == -1:
        lref.insert(0, len(self.bookstore))
        self.bookstore.append(lref)
        treeview().full_list.append(ref)
        treeview.row_num = len(self.bookstore)
      else:
        try:
          lref.insert(0, self.indx)
          self.bookstore.insert(self.indx, lref)
          treeview().full_list[self.indx] = ref
          # print(treeview().full_list[:])
        except TypeError:
          self.bookstore.append(lref)
          treeview().full_list[-1] = ref
    self.current_filter_language = None
    return treeview.row_num

  def row_activated(self, widget, row, col):
    self.row = row
    (model, path) = widget.get_selection().get_selected_rows()
    tree_iter = model.get_iter(path)
    self.indx = model.get_value(tree_iter, 0)
    slist = list(zip(self.entries, model[row][1:]))
    # print(slist[-1][-1])
    # self.treeview.remove(row)
    return True

  def edit_clicked(self, widget, row, col):
    self.row = row
    (model, path) = widget.get_selection().get_selected_rows()
    tree_iter = model.get_iter(path)
    self.indx = model.get_value(tree_iter, 0)
    slist = list(zip(self.entries, model[row][1:]))
    self.retrieve_treeview(slist)

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

  def retrieve_treeview(self, slist):
    self.popup = Gtk.Window()
    self.popup.set_border_width(2)
    popheader = Gtk.HeaderBar()
    self.popup.set_titlebar(popheader)
    popheader.set_title(str(self.indx))
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
    for i, viewcol in enumerate(["Field", "Value"]):
      vrenderer = Gtk.CellRendererText()
      if i == 1:
        vrenderer.set_property("wrap-width", 300)
        vrenderer.set_property("editable", True)
      vcolumn = Gtk.TreeViewColumn(viewcol, vrenderer, text=i)
      tview.append_column(vcolumn)
    vrenderer.connect("edited", self.val_edited)
    self.slist = slist
    for keyval in self.slist:
      self.viewstore.append(list(keyval))
    file_button = Gtk.Button("Add File")
    file_button.connect("clicked", self.insert_file_val)
    scrolw.add(tview)
    grid.attach(scrolw, 0, 0, 2, 1)
    grid.attach(self.updater, 0, 1, 1, 1)
    grid.attach(file_button, 1, 1, 1, 1)
    self.popup.add(grid)
    self.popup.show_all()

  def insert_file_val(self, widget):
    self.cell.file_attach_cb()
    self.val_list = [i[1] for i in self.slist]
    self.Files.move_file(self.cell.file_name, self.val_list)
    self.viewstore[-1][1] = os.path.basename(self.Files.destin)
    self.val_list[-1] = os.path.basename(self.Files.destin)
    self.updater.set_sensitive(True)

  def val_edited(self, widget, path, text):
    self.viewstore[path][1] = text
    self.val_list = [i[1] for i in self.slist]
    self.val_list[int(path)] = text
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
