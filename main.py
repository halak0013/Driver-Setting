from main_window import Main_Window
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk as g



window=Main_Window()
window.connect("destroy",g.main_quit)
window.show_all()
g.main()