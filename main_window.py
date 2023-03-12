# Bismillahirrahmanirrahim
import webbrowser
from fonksiyonlar import *
from gi.repository import Gtk as g, Gdk
import gi
gi.require_version("Gtk", "3.0")


class Main_Window(g.Window):
    def __init__(self):
        g.Window.__init__(self, title="Sürücü Ayarları")
        self.bx_main = g.HBox(spacing=6)
        self.bx_options = g.VBox(spacing=6)
        self.bx_setting = g.VBox(spacing=6)
        self.bx_brightnes = g.HBox(spacing=6)


        self.add(self.bx_main)
        self.bx_main.add(self.bx_options)
        self.bx_main.add(self.bx_setting)

        """ self.rd_bt_a_kaynak = g.RadioButton.new_with_label_from_widget(
            None, "açık kaynak") """
        self.rd_bt_p_source = g.RadioButton(label="kapalı kaynak")

        self.rd_bt_not_cuda = g.RadioButton.new_with_label_from_widget(
            None, "cuda olmadan")
        self.rd_bt_with_cuda = g.RadioButton.new_with_label_from_widget(
            self.rd_bt_not_cuda, "cuda ile")

        self.bt_install = g.Button(label="yükle")
        self.bt_install.connect("clicked", self.on_click_install)

        self.bt_how = g.Button(label="Nasıl Kullanılır")
        self.bt_how.connect("clicked", self.on_click_how)

        self.bt_web = g.Button(label="İnternet adresi")
        self.bt_web.connect("clicked", self.web_fun)

        self.list_ = (self.rd_bt_p_source, self.rd_bt_not_cuda,
                      self.rd_bt_with_cuda, self.bt_install, self.bt_how, self.bt_web)
        for ele in self.list_:
            self.bx_options.pack_start(ele, True, True, 3)

        self.lb_type = g.Label("Grafik birimi")
        self.bx_graphic = g.HBox(spacing=0)

        self.bt_nvidia = g.Button(label="Nvidia")
        self.bt_nvidia.connect("clicked", self.nvidia_fun)

        self.bt_entegre = g.Button(label="Tümleşik grafik")
        self.bt_entegre.connect("clicked", self.entegre_fun)

        self.bx_graphic.pack_start(self.bt_nvidia, True, True, 3)
        self.bx_graphic.pack_start(self.bt_entegre, True, True, 3)

        self.bt_both = g.Button(label="İkisi bir arada")
        self.bt_both.connect("clicked", self.both_fun)


        self.rbt_list=[]
        for bt in get_devices():
            self.rbt_list.append(g.CheckButton.new_with_label(bt))
            self.bx_brightnes.pack_start(self.rbt_list[-1], True, True, 3)
        
        self.scl_level=g.Scale.new_with_range(g.Orientation.HORIZONTAL,0,1.0,0.05)
        self.scl_level.set_value(1)
        self.scl_level.connect("value-changed", self.on_scl_brigh_change)


        self.lb_output = g.Label("İşlem çıktıları burada gözükür")

        self.sld_output = g.ScrolledWindow()
        self.sld_output.set_policy(
            g.PolicyType.AUTOMATIC, g.PolicyType.AUTOMATIC)
        self.sld_output.set_size_request(200, 100)
        self.sld_output.add(self.lb_output)

        self.list_ = (self.lb_type, self.bx_graphic, 
                      self.bt_both,self.bx_brightnes,self.scl_level, self.sld_output)
        for ele in self.list_:
            self.bx_setting.pack_start(ele, True, True, 3)
        
        if get_display_m() == "GNOME":
            warning("""
Değerli Kullanıcı
Gnome kullanırken eski grafik birimi kaldırılırken
Bazen sistem çöktü hatası gelebiliyor çıkış deyip tekrar
yükleye basrasanız yüklemeye devam edcektir inşAllah

Ek olarak yüklendikten yeniden başlatınca 
girişten wyland olmayan gnomu seçmeniz gerekmektedir
""")
        warning("""
            Değerli Kullanıcı
            1 yükleme
            2 grafik birimleri arasında geçiş
            Uyarı!
            yükleme sırasında sddm giriş ekranı yükleniyor
            Lütfen sddm'yi sçmeyi unutmayın!
            Uygulama iki aşamadan oluşur
            yükleme direk nividia depolarından yükleniyor. Ve gerekli
            ayarlar yapılıyor.

            Grafik birimi arasında geçiş yaparken:
            Nvidia: tüm işlemler nvidia kartında gerçekleşir
            İksi bir arada: Nvidia ve tümleşik(işlemcideki) birimde gerçekleşir
            Tümleşik: tüm işlemler sadece tümleşik(işlemcideki) birimde gerçekleşir
            """)

    def on_click_install(self, widget):
        """ if self.rd_bt_a_kaynak.get_active():
            if self.rd_bt_v_cuda.get_active():
                yukle(A_CV)
            else:
                yukle(A_CY)
        else: """
        if self.rd_bt_with_cuda.get_active():
            install(K_CV)
        else:
            install(K_CY)

    def on_click_how(self, widget):
        warning("""Nasıl çalışır
        
- Program sizin yerinize 
    - gerekli nevidia depolarını sisteminize ekleyerek,
    - gerekli paketleri yükleyerek
    - giriş ekran ayarlarını yaparak
    yüklemeyi yapar
- grafik kartı geçişi envycontrol ile birilkte yapılıyor
    - nvidia modu 
    - envycontrol https://github.com/bayasdev/envycontrol
    - geçiş işlemi ilk olarak ikili moda geçilmesi gerekiyor
""")

    def web_fun(self, widget):
        webbrowser.open("https://github.com/halak0013/Driver-Setting")

    def nvidia_fun(self, widget):
        change("nvidia")

    def entegre_fun(self, widget):
        change("integrated")

    def both_fun(self, widget):
        change("hybrid")

    def on_scl_brigh_change(self,widget):
        for p in self.rbt_list:
            if p.get_active():
                change_brightness(p.get_label(),widget.get_value())

