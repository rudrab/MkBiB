import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class MessageDialog(Gtk.Window):

    # def __init__(self):
        # Gtk.Window.__init__(self, title="MessageDialog Example")

        # box = Gtk.Box(spacing=6)
        # self.add(box)

        # button1 = Gtk.Button("Information")
        # button1.connect("clicked", self.on_info_clicked)
        # box.add(button1)

        # button2 = Gtk.Button("Error")
        # button2.connect("clicked", self.on_error_clicked)
        # box.add(button2)

        # button3 = Gtk.Button("Warning")
        # button3.connect("clicked", self.on_warn_clicked)
        # box.add(button3)

        # button4 = Gtk.Button("Question")
        # button4.connect("clicked", self.on_question_clicked)
        # box.add(button4)

    def on_info_clicked(self, widget):
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,
            Gtk.ButtonsType.OK, "This is an INFO MessageDialog")
        dialog.format_secondary_text(
            "And this is the secondary text that explains things.")
        dialog.run()
        print("INFO dialog closed")

        dialog.destroy()

    def on_error_clicked(self, err_str1, err_str2):
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR,
            Gtk.ButtonsType.CANCEL, err_str1)
        dialog.format_secondary_text(err_str2)
        dialog.run()
        dialog.destroy()

    def on_warn_clicked(self, err_str1, err_str2):
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING,
            Gtk.ButtonsType.OK, err_str1)
        dialog.format_secondary_text(err_str2)
        response = dialog.run()
        dialog.destroy()

    def on_question_clicked(self, widget):
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.QUESTION,
            Gtk.ButtonsType.YES_NO, "This is an QUESTION MessageDialog")
        dialog.format_secondary_text(
            "And this is the secondary text that explains things.")
        response = dialog.run()
        if response == Gtk.ResponseType.YES:
            print("QUESTION dialog closed by clicking YES button")
        elif response == Gtk.ResponseType.NO:
            print("QUESTION dialog closed by clicking NO button")

        dialog.destroy()

class PopWindow():
    def popup(self):
        self.popup = Gtk.Window()
        self.popup.set_border_width(2)
        self.popheader = Gtk.HeaderBar()
        self.popup.set_titlebar(self.popheader)
        # popheader.set_title(indx)
        self.popup.set_default_size(450, 550)
        self.popheader.set_show_close_button(True)

