from envycontrol import *
import os
import subprocess

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk as g


A_CV = 0
A_CY = 1
K_CV = 2
K_CY = 3

#? getting screen name
def get_devices():
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

#? setting alert
def query(text):
    dialog = g.Dialog(title="Uyarı!", parent=None, flags=0)
    dialog.add_button("Evet", g.ResponseType.YES)
    dialog.add_button("Hayır", g.ResponseType.NO)
    label = g.Label()
    label.set_text(f"""
    {text}
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

#? alert dialog
def warning(text):
    dialog = g.MessageDialog(flags=0,
                             message_type=g.MessageType.INFO,
                             buttons=g.ButtonsType.OK)
    dialog.set_icon_from_file("/usr/share/icons/psy.png")
    dialog.format_secondary_text(text)
    dialog.run()
    dialog.destroy()

#? changing gpu mode
def change(mode):
    display_manager = check_display_manager()
    # switcher(mode)
    print(display_manager)
    add = ""
    location = getLocation()
    print(location)
    if display_manager == "sddm":
        add = "--dm sddm"
    cmd = f"""#!/bin/bash
echo 'Lütfen şifrenizi giriniz'
sudo python3 {location}/envycontrol.py -s {mode} {add}
exit
"""
    print(cmd)
    subprocess.Popen(['x-terminal-emulator', '-e',
                      f'bash -c "echo \'{cmd}\' > betik.sh && chmod +x betik.sh && ./betik.sh; exec bash"'], cwd="/tmp/")


def get_display_m():
    return os.environ.get('XDG_CURRENT_DESKTOP')

#? installing nvidia driver
def install(type):
    location = getLocation()
    print(location)
    display_managet = get_display_m()
    gnome_error = ""
    if display_managet == "GNOME":
        gnome_error = f"""
sudo rm -f /usr/libexec/gnome-session-failed
sudo cp -f {location}/gnome-session-failed /usr/libexec/
sudo chmod +x /usr/libexec/gnome-session-failed
"""
    cmd = f"""#!/bin/bash
echo 'İşlem bittikten sonra bilgisyar yeniden başlatılacaktır'
echo 'Lütfen açık olan uygulamalarınızı kapatın'
echo 'Lütfen şifrenizi giriniz'
sudo apt update && sudo apt upgrade -y
sudo apt install sddm -y
{gnome_error}
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
    if type == A_CV:
        cmd += "sudo apt install nvidia-driver cuda nvidia-kernel-open-dkms nvidia-smi nvidia-settings -y"
    elif type == A_CY:
        cmd += "sudo apt install nvidia-driver nvidia-kernel-open-dkms nvidia-smi nvidia-settings -y"
    elif type == K_CV:
        cmd += "sudo apt install nvidia-driver cuda nvidia-smi nvidia-settings -y"
    else:
        cmd += "sudo apt install nvidia-driver nvidia-smi nvidia-settings -y"
    cmd += "\nsudo apt purge xserver-xorg-video-nouveau -y \nsleep 5\nsudo reboot"
    print(cmd)
    subprocess.Popen(['x-terminal-emulator', '-e',
                     f'bash -c "echo \'{cmd}\' > betik.sh && chmod +x betik.sh && ./betik.sh; exec bash"'], cwd="/tmp/")


def change_brightness(window, val):
    cmd = f"xrandr --output {window} --brightness {val}"
    subprocess.run(cmd.split(), check=True)


def getLocation():
    if os.path.exists("/opt/surucu-ayar/envycontrol.py"):
        return "/opt/surucu-ayar"
    else:
        return os.getcwd()
