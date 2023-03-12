from main_window import Main_Window
import gi
import os
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk as g



window=Main_Window()
location="/usr/share/icons" if os.path.exists("/opt/surucu-ayar/envycontrol.py") else os.getcwd()
window.set_default_icon_from_file(f"{location}/psy.png")
window.connect("destroy",g.main_quit)
window.show_all()
g.main()