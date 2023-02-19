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
    komut = f"""sudo python3 {konum}/envycontrol.py -s {mode} {ekle}
exit
"""
    subprocess.Popen(['x-terminal-emulator', '-e',
                      f'bash -c "echo \'{komut}\' > betik.sh && chmod +x betik.sh && ./betik.sh; exec bash"'], cwd="/tmp/")



def yukle(tur):
    konum = os.getcwd()
    komut = f"""#!/usr/bin/bash

sudo apt purge nvidi* xserver-xorg-video-nouveau -y
sudo apt install dirmngr ca-certificates software-properties-common apt-transport-https dkms curl unzip -y
curl -fSsL https://developer.download.nvidia.com/compute/cuda/repos/debian11/x86_64/3bf863cc.pub | sudo gpg --dearmor | sudo tee /usr/share/keyrings/nvidia-drivers.gpg > /dev/null 2>&1
echo 'deb [signed-by=/usr/share/keyrings/nvidia-drivers.gpg] https://developer.download.nvidia.com/compute/cuda/repos/debian11/x86_64/ /' | sudo tee /etc/apt/sources.list.d/nvidia-drivers.list
sudo add-apt-repository contrib
sudo apt update
sudo apt install sddm -y
"""
    if tur == A_CV:
        komut += "sudo apt install nvidia-driver cuda nvidia-kernel-open-dkms nvidia-smi nvidia-settings -y"
    elif tur == A_CY:
        komut += "sudo apt install nvidia-driver nvidia-kernel-open-dkms nvidia-smi nvidia-settings -y"
    elif tur == K_CV:
        komut += "sudo apt install nvidia-driver cuda nvidia-smi nvidia-settings -y"
    else:
        komut += "sudo apt install nvidia-driver nvidia-smi nvidia-settings -y"
    print(komut)
    subprocess.Popen(['x-terminal-emulator', '-e',
                     f'bash -c "echo \'{komut}\' > betik.sh && chmod +x betik.sh && ./betik.sh; exec bash"'], cwd="/tmp/")
