import gi
import os
import webbrowser
import Mkbib.dialogue as dialogue
import shutil
from gi.repository import Gtk
import subprocess
import re
gi.require_version("Gtk", "3.0")


class file_manager():
    # slist = ""
    def __init__(self):
        self.Messages = dialogue.MessageDialog()
        self.Dialog = dialogue.FileDialog()
    # Before starting,
    # Check if root exists
    def chk_rootdir(self):
        global basedir
        rootdir = "/var/tmp"
        basedir = rootdir+"/Mkbib"
        if not os.path.exists(basedir):
            os.makedirs(basedir)
            self.root_status = (basedir +" Created.")
        else:
            self.root_status = (basedir +" already exists.")

    def chk_subdir(self, filename):
        global subdir
        subdir = basedir+"/"+filename
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
