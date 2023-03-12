from main_window import Main_Window
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk as g



window=Main_Window()
window.set_default_icon_from_file("/usr/share/icons/psy.png")
window.connect("destroy",g.main_quit)
window.show_all()
g.main()