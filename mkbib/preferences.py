###########################################
# Preferences
# Author: Rudra Banerjee
# Last Update: 20/09/2016
#
# Managing files and preferences
# License: GPLv3
###########################################
import gi
import os
import webbrowser
import Mkbib.dialogue as dialogue
# import Mkbib.menu as menu
import shutil
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio
import subprocess
import re


class file_manager():
    # slist = ""
    def __init__(self):
        self.Messages = dialogue.MessageDialog()
        self.Dialog = dialogue.FileDialog()
    # Before starting,
    # Check if root exists
    def chk_rootdir(self):
        self.setting = Gio.Settings.new("org.example.mkbib")
        # self.setting.bind("base-folder", self.user_dir, "label", Gio.SettingsBindFlags.DEFAULT)
        basedir = self.setting.get_string("base-folder")
        # global basedir
        self.basedir = basedir+"/Mkbib"
        # self.basedir = self.setting.get_value("base-folder")
        # self.root_status = "HI"
        if not os.path.exists(self.basedir):
            os.makedirs(self.basedir)
            self.root_status = (self.basedir +" Created.")
        else:
            self.root_status = (self.basedir +" already exists.")

    def chk_subdir(self, filename):
        global subdir
        subdir = self.basedir+"/"+filename
        print(subdir)
        if not os.path.exists(subdir):
            os.makedirs(subdir)
            self.base_status = (subdir +" Created.")
        else:
            self.base_status = (subdir +" already exists.")

    def move_file(self, source, destin):
        # print(subdir)
        # print(source)
        destin = destin[2].replace(" ", "_")+"_"+destin[3].split()[0]+"_"+str(destin[5])#+os.path.splitext(source)[1]
        destin = re.sub('[^A-Za-z0-9_-]+', '', destin)+os.path.splitext(source)[1]
        self.destin = subdir+"/"+destin
        shutil.copy(source, self.destin)

    def open_file(self, doc):
        print(subdir+"/"+doc)
        subprocess.call(["xdg-open", subdir+"/"+doc])

    def preferences(self, err1, err2):
        Wpref =  Gtk.Window(border_width=5)
        prefheader = Gtk.HeaderBar()
        prefheader.set_subtitle("Preferences")
        prefheader.set_title("Mkbib")
        Wpref.set_titlebar(prefheader)
        prefheader.set_show_close_button(True)
        menuicon = Gtk.Image.new_from_icon_name("preferences-desktop-symbolic", Gtk.IconSize.MENU);
        Gtk.HeaderBar.pack_start(prefheader,menuicon);

        Wpref.set_default_size(350, 350)
        grid = Gtk.Grid(column_spacing=20)
        Wpref.add(grid)
        dir_label = Gtk.Label("Set user dir:")
        self.user_dir =Gtk.Button()
        self.user_dir.set_always_show_image(True)
        self.user_dir.set_image(image=Gtk.Image(
                icon_name="folder-open-symbolic"))
        self.user_dir.set_image_position(1)
        self.user_dir.connect("clicked", self.set_folder_clicked)
        self.setting = Gio.Settings.new("org.example.mkbib")
        self.setting.bind("base-folder", self.user_dir, "label", Gio.SettingsBindFlags.DEFAULT)
        self.basedir = self.setting.get_value("base-folder")
        # print("From"+str(self.basedir))
        grid.attach(dir_label, 0, 1, 1, 1)
        grid.attach(self.user_dir, 1, 1, 1, 1)
        Wpref.show_all()

    def set_folder_clicked(self, name):
        self.Dialog.FileChooser(["Choose Folder",
                                 "", "", False],
                                Gtk.FileChooserAction.SELECT_FOLDER, "Select")
        if self.Dialog.response == Gtk.ResponseType.OK:
            self.filename = self.Dialog.dialog.get_filename()
            self.user_dir.set_label(self.filename)
            self.Dialog.dialog.destroy()
            self.Messages.on_info_clicked("Setting Updated", "Restart MkBiB to enable changes.")
        elif self.Dialog.response == Gtk.ResponseType.CANCEL:
            self.Dialog.dialog.destroy()

