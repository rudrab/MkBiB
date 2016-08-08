import gi
from gi.repository import Gtk
from gi.repository import GdkPixbuf
gi.require_version('Gtk', '3.0')

class MessageDialog(Gtk.Window):


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

    def about_activated(self, action, data=None):
        copyright = "Copyright \u00a9 2016- - Rudra Banerjee"
        comments = "BiBTeX Manager"
        dialog = Gtk.AboutDialog(program_name="MkBiB", transient_for=self,
                                 name="About MkBiB",
                                 comments=comments,
                                 version="0.1",
                                 copyright=copyright,
                                 license_type=Gtk.License.GPL_3_0,
                                 authors=(["Rudra Banerjee"]),
                                 website="https://github.com/rudrab/mkbib")
        # dialog.set_transient(Window)
        dialog.set_logo(GdkPixbuf.Pixbuf.new_from_file_at_size(
            "/home/rudra/Devel/Icons/shadow/scalable/apps/mkbib.svg", 128, 128)
        )
        dialog.run()
        dialog.destroy()

# class PopWindow():
#     def popup(self):
#         self.popup = Gtk.Window()
#         self.popup.set_border_width(2)
#         self.popheader = Gtk.HeaderBar()
#         self.popup.set_titlebar(self.popheader)
#         # popheader.set_title(indx)
#         self.popup.set_default_size(450, 550)
#         self.popheader.set_show_close_button(True)



class FileDialog(Gtk.Window):
    # File Chooser
    # Open, Save
    def FileChooser(self, header, action):
        self.path = None
        self.dialog = Gtk.FileChooserDialog(header[0], self,
                                       action,
                                       (Gtk.STOCK_CANCEL,
                                        Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        filter = Gtk.FileFilter()
        filter.set_name(header[1])
        filter.add_pattern(header[2])
        self.dialog.add_filter(filter)
        filter = Gtk.FileFilter()
        filter.set_name("All Files")
        filter.add_pattern("*")
        self.dialog.add_filter(filter)

        self.response = self.dialog.run()

def close_window(self, widget):
    widget.destroy()
