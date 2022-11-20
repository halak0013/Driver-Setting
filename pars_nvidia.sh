#!/bin/bash

##
user=$(whoami)
FILE=/home/$user/pars_nvidia_log.txt
ENVI=""
LOG=""
if test -f "$FILE"; then
    sudo bash -c -i '
    DESKTOP=(""$(cat /etc/X11/default-display-manager))
    modprobe -r nouveau &&
	LOG+="
	modprobe -r nouveau işlemi yapıldı
	" &&
    ## nvidia yazılımı çalışırken x org ile çakkışmasın diye
    ## servisi durduruyoruz
    ## bu xfce sistemi için geçerli 
    ## gnome için lightdm yerine gdm kullanılamsı gerekiyor
    case $DESKTOP in
	"/usr/sbin/lightdm")
	ENVI="lightdm"
	;;
	"/usr/sbin/gdm3")
	ENVI="gdm3"
	;;
	"/usr/sbin/sddm")
	ENVI="sddm"
	;;
	"/usr/sbin/gdm3")
	ENVI="gdm3"
	;;
	*)
	echo "hatalı giriş yapıldı"
	exit
	;;
    esac
	LOG+="
	case ile masaüstü seçildi $DESKTOP
	" &&
    	service $ENVI stop
	LOG+="
	x11 duruduruldu
	" &&
    	sh NVIDIA-Linux-x86_64* &&
	LOG+="
	yükleme bitti" &&
    echo "
    $LOG
    " >> $FILE ;
	reboot
    '
else
    sudo bash -c  -i '
    apt update -y &&
    apt upgrade -y &&
	LOG+="
	güncellemeler yapıldı" &&
    ##derleme için gerekli karnel paketleri yüklemesi
    apt install linux-headers-$(uname -r) -y &&
	LOG+="
	kerenel başlıkları yüklendi" &&
    apt install linux-source dkms build-essential -y &&
	LOG+="
	kernel bağımlılıkları yüklendi" &&
    ##nvidia sitesindeki gereklilikler
    apt install libglvn* libvdpau* libvulkan* make gcc -y &&
    	LOG+="
	nvidia gereklilikleri yüklendi" &&
    ##pardus nvidianın  nouveau driveri ile çalışmasını engellemek için
    apt purge nvidi* xserver-xorg-video-nouveau -y &&
	LOG+="
	eski nvidia bağımlılıkları silindi"
    '
    

    echo "
    blacklist nouveau
    options nouveau modeset=0
    " > blacklist.conf

    ## gerekli temel ayarlar yapıldıktan sonra tekrar aynı yerden başlamaması için
    ## kullanıcıda bir log oluşturyor  hata veya yapılandırma 
    ## kayırtları eklenir
    echo "
    $LOG
    " >> $FILE
    
    
    sudo bash -c  -i '
    ##configin taşınması
    cp blacklist.conf /etc/modprobe.d/blacklist.conf &&

    ##gerekirse bazı güncellemeleri yapması için
    update-initramfs -u &&
    echo "bilgisayar birazdan yeniden başlayacaktır" &&
    sleep 2 &&
    echo "
    $LOG
    " >> $FILE ;
    reboot
    '
fi
    echo "
    $LOG
    " >> $FILE
