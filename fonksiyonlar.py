import os
import subprocess

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk as g

from envycontrol import *

A_CV = 0
A_CY = 1
K_CV = 2
K_CY = 3


def cihazlariGetir():
    # xrandr çıktısını alın
    xrandr_output = subprocess.check_output(['xrandr']).decode('utf-8')

    # Satırları listeye ayırın
    lines = xrandr_output.strip().split('\n')

    # Satırların her birini işleyin ve cihaz isimlerini bir listeye ekleyin
    devices = []
    for line in lines:
        if ' connected ' in line:
            device_name = line.split()[0]
            devices.append(device_name)
    return devices

def sorgu(metin):
    dialog = g.Dialog(title="Uyarı!", parent=None, flags=0)
    dialog.add_button("Evet", g.ResponseType.YES)
    dialog.add_button("Hayır", g.ResponseType.NO)
    label = g.Label()
    label.set_text(f"""
    {metin}
    """)

    box = dialog.get_content_area()
    box.add(label)

    dialog.show_all()

    response = dialog.run()
    if response == g.ResponseType.YES:
        dialog.destroy()
        return 'evet'
    elif response == g.ResponseType.NO:
        dialog.destroy()
        return 'hayır'


def uyari(metin):
    dialog = g.MessageDialog(flags=0,
                             message_type=g.MessageType.INFO,
                             buttons=g.ButtonsType.OK)
    dialog.format_secondary_text(metin)
    dialog.run()
    dialog.destroy()


def degistir(mode):
    goruntu_yoneticisi = check_display_manager()
    # switcher(mode)
    print(goruntu_yoneticisi)
    ekle = ""
    konum = os.getcwd()
    if goruntu_yoneticisi == "sddm":
        ekle = "--dm sddm"
    komut = f"""#!/bin/bash
echo 'Lütfen şifrenizi giriniz'
sudo python3 {konum}/envycontrol.py -s {mode} {ekle}
exit
"""
    subprocess.Popen(['x-terminal-emulator', '-e',
                      f'bash -c "echo \'{komut}\' > betik.sh && chmod +x betik.sh && ./betik.sh; exec bash"'], cwd="/tmp/")

def m_ortami():
    return os.environ.get('XDG_CURRENT_DESKTOP')

def yukle(tur):
    konum = os.getcwd()
    masaustu_ortami = m_ortami()
    gnome_hata=""
    if masaustu_ortami == "GNOME":
        gnome_hata=f"""
sudo rm -f /usr/libexec/gnome-session-failed
sudo cp -f {konum}/gnome-session-failed /usr/libexec/
sudo chmod +x /usr/libexec/gnome-session-failed
"""
    komut = f"""#!/bin/bash
echo 'İşlem bittikten sonra bilgisyar yeniden başlatılacaktır'
echo 'Lütfen açık olan uygulamalarınızı kapatın'
echo 'Lütfen şifrenizi giriniz'
sudo apt update && sudo apt upgrade -y
sudo apt install sddm -y
{gnome_hata}
sleep 5
sudo apt purge nvidia* -y
sleep 5
sudo apt install dirmngr ca-certificates software-properties-common apt-transport-https dkms curl unzip -y
sleep 5
curl -fSsL https://developer.download.nvidia.com/compute/cuda/repos/debian11/x86_64/3bf863cc.pub | sudo gpg --dearmor | sudo tee /usr/share/keyrings/nvidia-drivers.gpg > /dev/null 2>&1
echo 'deb [signed-by=/usr/share/keyrings/nvidia-drivers.gpg] https://developer.download.nvidia.com/compute/cuda/repos/debian11/x86_64/ /' | sudo tee /etc/apt/sources.list.d/nvidia-drivers.list
sleep 5
sudo add-apt-repository contrib
sudo apt update
sleep 5
"""
    if tur == A_CV:
        komut += "sudo apt install nvidia-driver cuda nvidia-kernel-open-dkms nvidia-smi nvidia-settings -y"
    elif tur == A_CY:
        komut += "sudo apt install nvidia-driver nvidia-kernel-open-dkms nvidia-smi nvidia-settings -y"
    elif tur == K_CV:
        komut += "sudo apt install nvidia-driver cuda nvidia-smi nvidia-settings -y"
    else:
        komut += "sudo apt install nvidia-driver nvidia-smi nvidia-settings -y"
    komut+="\nsudo apt purge xserver-xorg-video-nouveau -y \nsleep 5\nsudo reboot"
    print(komut)
    subprocess.Popen(['x-terminal-emulator', '-e',
                     f'bash -c "echo \'{komut}\' > betik.sh && chmod +x betik.sh && ./betik.sh; exec bash"'], cwd="/tmp/")
