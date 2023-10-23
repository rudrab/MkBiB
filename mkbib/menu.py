###########################################
# menu.py
# Author: Rudra Banerjee
# Last Update: 02/09/2016
#
# Organize menu items and functions
# License: GPLv3
###########################################
import io
# import Mkbib.preferences as preferences
import os
import subprocess

import gi
import Mkbib.cell as cell
import Mkbib.dialogue as dialogue
import Mkbib.pybib as pybib
import Mkbib.view as view

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio  # isort:skip


class MenuManager(Gtk.Window):

  def __init__(self):
    self.parsing = pybib.parser()
    self.TreeView = view.treeview()
    self.Dialog = dialogue.FileDialog()
    self.cell = cell.cell_renderer()
    # self.Files = preferences.file_manager()

  def file_new_clicked(self, widget):
    dialog = Gtk.FileChooserDialog("Open an existing fine", None,
                                   Gtk.FileChooserAction.OPEN,
                                   (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                    Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
    response = dialog.run()
    if response == Gtk.ResponseType.OK:
      self.filename = dialog.get_filename()
      return (self.filename)
    elif response == Gtk.ResponseType.CANCEL:
      print("Cancel clicked")

    dialog.destroy()

  def create_textview(self, SimpleAction, parameter):
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
    textbuffer = tview.get_buffer()
    scrolw.add(tview)
    grid.attach(scrolw, 0, 0, 10, 10)
    grid.attach(button, 0, 11, 10, 1)
    button.connect("clicked", self.create_from_buffer, textbuffer, popup)
    popup.add(grid)
    popup.show_all()

  def import_format(self, SimpleAction, parameter):
    popup = Gtk.Window(border_width=5)
    popup.set_title("Import to BiBTeX")
    popup.set_default_size(350, 350)
    grid = Gtk.Grid()
    scrolw = Gtk.ScrolledWindow()
    scrolw.set_hexpand(True)
    scrolw.set_vexpand(True)
    buttonRIS = Gtk.Button("From RIS")
    tview = Gtk.TextView()
    tview.set_wrap_mode(Gtk.WrapMode.WORD)

    # Get the buffer
    self.textbuffer = tview.get_buffer()
    scrolw.add(tview)
    grid.attach(scrolw, 0, 0, 10, 10)
    grid.attach(buttonRIS, 0, 11, 10, 1)
    # buttonRIS.connect("clicked", self.create_from_buffer, textbuffer, popup)
    buttonRIS.connect("clicked", self.import_ris)
    popup.add(grid)
    popup.show_all()

  def import_ris(self, textbuffer):
    p1 = subprocess.Popen(["ris2xml", "/var/tmp/nphys3271.ris"],
                          stdout=subprocess.PIPE)
    with open("bib.bib", "w") as out:
      p2 = subprocess.Popen(["xml2bib"], stdin=p1.stdout, stdout=out)
    print(p2)

  def create_from_buffer(self, widget, textbuffer, window):
    start_iter = textbuffer.get_start_iter()
    end_iter = textbuffer.get_end_iter()
    text = textbuffer.get_text(start_iter, end_iter, True)
    del self.parsing.booklist[:]
    self.parsing.parsing_read(text)
    self.TreeView.viewer(self.parsing.booklist)
    window.destroy()

  # def preferences(self, err1, err2):
  # Wpref =  Gtk.Window(border_width=5)
  # prefheader = Gtk.HeaderBar()
  # prefheader.set_title("Preferences")
  # Wpref.set_titlebar(prefheader)
  # prefheader.set_show_close_button(True)
  # menuicon = Gtk.Image.new_from_icon_name("preferences-desktop-symbolic", Gtk.IconSize.MENU);
  # Gtk.HeaderBar.pack_start(prefheader,menuicon);

  # Wpref.set_default_size(350, 350)
  # grid = Gtk.Grid(column_spacing=20)
  # Wpref.add(grid)
  # dir_label = Gtk.Label("Set user dir:")
  # self.user_dir =Gtk.Button()
  # self.user_dir.set_always_show_image(True)
  # self.user_dir.set_image(image=Gtk.Image(
  # icon_name="folder-open-symbolic"))
  # self.user_dir.set_image_position(1)
  # self.user_dir.connect("clicked", self.set_folder_clicked)
  # setting = Gio.Settings.new("org.example.mkbib")
  # setting.bind("base-folder", self.user_dir, "label", Gio.SettingsBindFlags.DEFAULT)
  # self.basedir = setting.get_value("base-folder")
  # print(self.basedir)
  # grid.attach(dir_label, 0, 1, 1, 1)
  # grid.attach(self.user_dir, 1, 1, 1, 1)
  # Wpref.show_all()

  # def set_folder_clicked(self, name):
  # self.Dialog.FileChooser(["Choose Folder",
  # "", "", False],
  # Gtk.FileChooserAction.SELECT_FOLDER, "Select")
  # if self.Dialog.response == Gtk.ResponseType.OK:
  # self.filename = self.Dialog.dialog.get_filename()
  # self.user_dir.set_label(self.filename)
  # self.Dialog.dialog.destroy()
  # elif self.Dialog.response == Gtk.ResponseType.CANCEL:
  # self.Dialog.dialog.destroy()
