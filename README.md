# Pardus-Debain-driver
Linux sistemlerde Nvida sürücülerinin yüklenmesi normal kullanıcı için zor olduğunda bunu için işi basitleştirmeye çalıştım inşAllah

# kod kısaca 
* gerekli çekirdek ve paket bağımlılıklarını yükleyip 
* tersine mühendislikle oluşturulan sürücülerini kaldırıp
* gerekli config ayarlarını yaptıktan sonra
* sistemi yeniden başlatıp
* masaüstü ortamına göre xOrg'u durdurup
* sürücüyü yüklüyor
* arada tekrarlamasın diye ve işlem adımlarını hataya karşı kayıt alıp ana klasörde kayıt tutuyor


# konular
* özet ve resimler
* yedek uyarısı
* kurulum hazırlığı
* sürücü kurulumu
* sonuç
* eksikler ve yapılması gerekenler
* son olarak

 # özet ve resimler
velhasıl benim gelebildiğim nokta 
xfce, gnome, kde, cinamon masaüstü ortamları olan Pardus veya Debian tabanlı sistemleri için kapalı kaynak sürcü kurulum
nvidianın kendi ayarları
![resim](https://user-images.githubusercontent.com/75750279/204157502-05292255-1531-4a23-9de7-61324af6ec66.png)
davinci 18
![resim](https://user-images.githubusercontent.com/75750279/204157510-0e4e7794-5c6d-4c06-b658-ad86de31d943.png)
blender ve nvidia-smi
![resim](https://user-images.githubusercontent.com/75750279/204157524-af44fa06-ddad-4c72-bd51-03e22a9f4d81.png)
Pardus hakkında ve neofetch
![resim](https://user-images.githubusercontent.com/75750279/204157534-4795b2eb-abd4-4ca7-becf-fb048be516f5.png)

# yedek uyarısı
!!!!
!!! Kurulum yapmak isterseniz öncelikle yedek almanızı kesinlikle tavsiye ederim. Herhangi hata çıkınca yardım etmeye çalışırız ancak sorumluluğun sizin üzerinizde olduğunu unutmayın!!!
!!!
yedek almak için de mağzadan timeshift programını yükleyerek yapabilirisiniz veya 
sudo apt install timeshift
ile ukurulum yapabilirsiniz

## Kurulum hazırlık
* İlk olarak <a href="https://www.nvidia.com.tr/drivers">Nvidianın sitesinden</a> cihazınız için uygun indermeniz gerekiyor
* İndirdikten sonra sürücüyü ev(home) yani kullanıcı klasörüne koymanız gerekiyor bu sıkıntı ilerki versiyonlarda inşAllah çözülmeye çalışılcak

* sonrasında <a href="https://github.com/halak0013/Pardus-Debain-driver/archive/refs/tags/driver.tar.gz">arşivi indirip</a> içindeki *pars_nvidia.sh* dosyasını ana ev klasörünze kopyalayın
![resim](https://user-images.githubusercontent.com/75750279/204157566-fe853fc9-e940-4e2b-89f6-c8efb59e0d93.png)


## Betik ile kurulum için 
* öncelikle uç birimi açıp dozyaları çalışabilir yapmak için
```chmod +x pars_nvidia.sh NVIDIA-Linux-*``` komutunu çalıştırmanız gerekiyor

*sonrasında crl alt f3 tuşlarına aynı anda basarak tty ekranını açıyoruz 
* kullanıcı ismimimzi yazıp sonrasında parolamızı yazıyoruz
*burada ```./pars_nvidia.sh``` yazmamız gerekiyor bunu yaparken tab tuşu ile tamamlama yapabiliriz

* bilgisayar yeniden başlayınca giriş yapmadan ctrl alt f3 tuşlarına aynı anda basıp tty ekranına geçiyoruz
* tekrardan kullanıcı ismimimzi yazıp sonrasında parolamızı yazıyoruz
* sonrasında ``./pars_nvidia.sh``` komutunu çalıştırıyoruz

## nvida kurulum ekranı gelince
* kernel modulünü dkms ile yükleyelim mi diye soruyor burada ok tuşları ile yes diyoruz
![resim](https://user-images.githubusercontent.com/75750279/202906832-2733303c-51dd-47ee-8053-82cf7c424c61.png)

* sonrasında 32 bit paketlerini yüklemek istiyor muyuz onu soruyor isteğinize göre yükleyebilirsiniz
![resim](https://user-images.githubusercontent.com/75750279/202906798-e8b20dc4-a72f-4beb-8113-fff4937d5963.png)

 - sonrasında zaten yüklenmeye başlayıp bitince de yeniden başlayacak inşAllah
 
Eğer herhangi bir hata alırsanız ev klasörünüzdeki pars_nvidia_log.txt içinedekiler ve mümkünse ekran görüntüsünü issue bölümünde paylaşırsanız yardımcı olmaya çalışırım
Şimdiden hayırlı olsun
