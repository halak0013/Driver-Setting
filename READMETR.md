# Sürücü Ayarları
Linux sistemlerde bazı sürücülerin yüklenmesi normal kullanıcı için zor olduğundan bu işi basitleştirmeye çalışıldı inşAllah

## Denen ve çalışan sistemler
- kde
- xfce
- gnome

Uygulama

![resim](https://user-images.githubusercontent.com/75750279/224530171-41b064f2-ed3e-4fde-9a63-f8e851380a7c.png)

## Nasıl çalışır
        
## program iki kısımdan oluşur
1-) sürücülerin yüklenmesi.

2-) istenen grafik moduna geçilmesi.

3-) ekranların parlaklıklarını değiştirme(şimdilik yeniden başlatınca eski haline geliyor)

## Çalıştırmak için
- program indermek ve klasörün  içinde terminal açıp 
- `python3 main.py` ile uygulama çalıştırılır.
- yükleye basılır
- gelen ekranda şifre girilir
- sddm için tamama basıp sddm seçilir
- son gelen novue... sürücüsü için uyarısan tamam denir
- sonrasında bilgisayar yeniden başlıyor.

## Uygulamanın çalışma prensibi

### yükleme kısımı için
- ilk önce sistem güncellenir
- sıkıntılı paketleri kaldırır
- gerekli bazı paketleri yükler
- nvidia deposunu ekler
- contrib depo aktifleştirilir
- depo güncellenir
- sonrasında seçilen moda göre cuda ile veya cudasız yükleme yapılır

### grafik kartı geçiş
- nvida seçilrse envycontrol ile gerekli ayarlamalar yapılıp sadece nvidianın calışmasını sağlanıyor
- tümleşik seçilirse sadece tümleşik(işlemci içindeki) birim çalışıyor
- ikili seçilirse hem nvidia hem de tümleşik birim aktifleşiyor.
    - bu modda blender ve davinci gibi gpu destekli programlar nvidiayı görebiliyor
    - ama geri kalan sistem gene tümleşik birimde çalışıyor



grafik kartı geçişi envycontrol https://github.com/bayasdev/envycontrol değiştirilerek yapılmıştır



istediğiniz moda tekar uygulamaya girip seçebilirsiniz

* nvidianın kendi ayarları

![resim](https://user-images.githubusercontent.com/75750279/204157502-05292255-1531-4a23-9de7-61324af6ec66.png)
![resim](https://user-images.githubusercontent.com/75750279/219940580-c8e98dbd-774d-4101-b8a4-4a0471052b36.png)


* davinci 18

![resim](https://user-images.githubusercontent.com/75750279/204157510-0e4e7794-5c6d-4c06-b658-ad86de31d943.png)

* blender ve nvidia-smi

![resim](https://user-images.githubusercontent.com/75750279/204157524-af44fa06-ddad-4c72-bd51-03e22a9f4d81.png)

* Pardus hakkında ve neofetch

![resim](https://user-images.githubusercontent.com/75750279/204157534-4795b2eb-abd4-4ca7-becf-fb048be516f5.png)

# yedek uyarısı
!!!!

Kurulum yapmak isterseniz öncelikle yedek almanızı kesinlikle tavsiye ederim. Herhangi hata çıkınca yardım etmeye çalışırız ancak sorumluluğun sizin üzerinizde olduğunu unutmayın

!!!

yedek almak için de mağzadan timeshift programını yükleyerek yapabilirisiniz veya 

```sudo apt install timeshift```


ile ukurulum yapabilirsiniz

Eğer herhangi bir hata alırsanız  ekran görüntüsünü issue bölümünde paylaşırsanız yardımcı olmaya çalışırım
Şimdiden hayırlı olsun
