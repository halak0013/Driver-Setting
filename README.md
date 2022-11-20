# Pardus-Debain-driver
Linux sistemlerde Nvida sürücülerinin yüklenmesi normal kullanıcı için zor olduğunda bunu için işi basitleştirmeye çalıştım inşAllah

## Kurulum hazırlık
* İlk olarak <a href="https://www.nvidia.com.tr/drivers">Nvidianın sitesinden</a> cihazınız için uygun indermeniz gerekiyor
* İndirdikten sonra sürücüyü ev(home) yani kullanıcı klasörüne koymanız gerekiyor bu sıkıntı ilerki versiyonlarda inşAllah çözülmeye çalışılcak

* sonrasında <a href="https://github.com/halak0013/Pardus-Debain-driver/archive/refs/tags/driver.tar.gz">arşivi indirip</a> içindeki *pars_nvidia.sh* dosyasını ana ev klasörünze kopyalayın

## Betik ile kurulum için 
* öncelikle uç birimi açıp dozyaları çalışabilir yapmak için
```chmod +x pars_nvidia.sh NVIDIA-Linux-*``` komutunu çalıştırmanız gerekiyor

*sonrasında crl alt f3 tuşlarına aynı anda basarak tty ekranını açıyoruz 
* kullanıcı ismimimzi yazıp sonrasında parolamizi yazıyoruz
*burada ```./pars_nvidia.sh``` yazmamız gerekiyor bunu yaparken tab tuşu ile tamamlama yapabiliriz

* bilgisayar yeniden başlayınca giriş yapmadan ctrl alt f3 tuşlarına aynı anda basıp tty ekranına geçiyoruz
* tekrardan ``./pars_nvidia.sh``` komutunu çalıştırıyoruz

## nvida kurulum ekranı gelince
* kernel modulünü dkms ile yükleyelim mi diye soruyor burada ok tuşları ile yes diyoruz
![resim](https://user-images.githubusercontent.com/75750279/202906832-2733303c-51dd-47ee-8053-82cf7c424c61.png)

* sonrasında 32 bit paketlerini yüklemek istiyor muyuz onu soruyor isteğinize göre yükleyebilirsiniz
![resim](https://user-images.githubusercontent.com/75750279/202906798-e8b20dc4-a72f-4beb-8113-fff4937d5963.png)

 -sonrasında zaten yüklenmeye başlıp bitince de yeniden başlayacak inşAllah
 
Eğer herhangi bir hata alırsanız ev klasörünüzdeki pars_nvidia_log.txt içinedekiler ve mümkünse ekran görüntüsünü issue bölümünde paylaşırsanız yardımcı olmaya çalışırım
Şimdiden hayırlı olsun
