# Bismillahirrahmanirrahim
import webbrowser
from fonksiyonlar import *
from gi.repository import Gtk as g, Gdk
import gi
gi.require_version("Gtk", "3.0")


class Ana_Ekran(g.Window):
    def __init__(self):
        g.Window.__init__(self, title="Pardus Sürücü Ayarları")
        self.ana_kutu = g.HBox(spacing=6)
        self.secenekler_kutu = g.VBox(spacing=6)
        self.ayarlamalar_kutu = g.VBox(spacing=6)

        self.add(self.ana_kutu)
        self.ana_kutu.add(self.secenekler_kutu)
        self.ana_kutu.add(self.ayarlamalar_kutu)

        """ self.rd_bt_a_kaynak = g.RadioButton.new_with_label_from_widget(
            None, "açık kaynak") """
        self.rd_bt_k_kaynak = g.RadioButton(label="kapalı kaynak")

        self.rd_bt_y_cuda = g.RadioButton.new_with_label_from_widget(
            None, "cuda olmadan")
        self.rd_bt_v_cuda = g.RadioButton.new_with_label_from_widget(
            self.rd_bt_y_cuda, "cuda ile")

        self.bt_yukle = g.Button(label="yükle")
        self.bt_yukle.connect("clicked", self.yukle_fun)

        self.bt_nasil = g.Button(label="Nasıl Kullanılır")
        self.bt_nasil.connect("clicked", self.nasil_fun)

        self.bt_web = g.Button(label="İnternet adresi")
        self.bt_web.connect("clicked", self.web_fun)

        self.liste = (self.rd_bt_k_kaynak, self.rd_bt_y_cuda,
                      self.rd_bt_v_cuda, self.bt_yukle, self.bt_nasil, self.bt_web)
        for ele in self.liste:
            self.secenekler_kutu.pack_start(ele, True, True, 3)

        self.lb_turu = g.Label("Grafik birimi")
        self.kutu_grafik = g.HBox(spacing=0)

        self.bt_nvidia = g.Button(label="Nvidia")
        self.bt_nvidia.connect("clicked", self.nvidia_fun)

        self.bt_entegre = g.Button(label="Tümleşik grafik")
        self.bt_entegre.connect("clicked", self.entegre_fun)

        self.kutu_grafik.pack_start(self.bt_nvidia, True, True, 3)
        self.kutu_grafik.pack_start(self.bt_entegre, True, True, 3)

        self.bt_ikisi = g.Button(label="İkisi bir arada")
        self.bt_ikisi.connect("clicked", self.ikisi_fun)

        self.lb_cikti = g.Label("İşlem çıktıları burada gözükür")

        self.kaydirabilir = g.ScrolledWindow()
        self.kaydirabilir.set_policy(
            g.PolicyType.AUTOMATIC, g.PolicyType.AUTOMATIC)
        self.kaydirabilir.set_size_request(200, 100)
        self.kaydirabilir.add(self.lb_cikti)

        self.liste = (self.lb_turu, self.kutu_grafik,
                      self.bt_ikisi, self.kaydirabilir)
        for ele in self.liste:
            self.ayarlamalar_kutu.pack_start(ele, True, True, 3)
        
        if m_ortami() == "GNOME":
            uyari("""
Değerli Kullanıcı
Gnome kullanırken eski grafik birimi kaldırılırken
Bazen sistem çöktü hatası gelebiliyor çıkış deyip tekrar
yükleye basrasanız yüklemeye devam edcektir inşAllah

Ek olarak yüklendikten yeniden başlatınca 
girişten wyland olmayan gnomu seçmeniz gerekmektedir
""")
        uyari("""
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

    def yukle_fun(self, widget):
        """ if self.rd_bt_a_kaynak.get_active():
            if self.rd_bt_v_cuda.get_active():
                yukle(A_CV)
            else:
                yukle(A_CY)
        else: """
        if self.rd_bt_v_cuda.get_active():
            yukle(K_CV)
        else:
            yukle(K_CY)

    def nasil_fun(self, widget):
        uyari("""Nasıl çalışır
        
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
        webbrowser.open("https://github.com/halak0013/Pardus-Debain-driver")

    def nvidia_fun(self, widget):
        degistir("nvidia")

    def entegre_fun(self, widget):
        degistir("integrated")

    def ikisi_fun(self, widget):
        degistir("hybrid")
