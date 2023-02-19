from ekran import Ana_Ekran
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk as g



pencere=Ana_Ekran()
pencere.connect("destroy",g.main_quit)
pencere.show_all()
g.main()