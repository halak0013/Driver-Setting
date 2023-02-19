#!/usr/bin/env python3
import argparse
import sys
import os
import re
import subprocess
#sys.path.append("../ana")

import fonksiyonlar

VERSION = '2.3'

BLACKLIST_PATH = '/etc/modprobe.d/blacklist-nvidia.conf'

BLACKLIST_CONTENT = '''# Automatically generated by EnvyControl

blacklist nouveau
blacklist nvidia
blacklist nvidia_drm
blacklist nvidia_uvm
blacklist nvidia_modeset
alias nouveau off
alias nvidia off
alias nvidia_drm off
alias nvidia_uvm off
alias nvidia_modeset off
'''

UDEV_INTEGRATED_PATH = '/lib/udev/rules.d/50-remove-nvidia.rules'

UDEV_INTEGRATED = '''# Automatically generated by EnvyControl

# Remove NVIDIA USB xHCI Host Controller devices, if present
ACTION=="add", SUBSYSTEM=="pci", ATTR{vendor}=="0x10de", ATTR{class}=="0x0c0330", ATTR{power/control}="auto", ATTR{remove}="1"

# Remove NVIDIA USB Type-C UCSI devices, if present
ACTION=="add", SUBSYSTEM=="pci", ATTR{vendor}=="0x10de", ATTR{class}=="0x0c8000", ATTR{power/control}="auto", ATTR{remove}="1"

# Remove NVIDIA Audio devices, if present
ACTION=="add", SUBSYSTEM=="pci", ATTR{vendor}=="0x10de", ATTR{class}=="0x040300", ATTR{power/control}="auto", ATTR{remove}="1"

# Remove NVIDIA VGA/3D controller devices
ACTION=="add", SUBSYSTEM=="pci", ATTR{vendor}=="0x10de", ATTR{class}=="0x03[0-9]*", ATTR{power/control}="auto", ATTR{remove}="1"
'''

UDEV_PM_PATH = '/lib/udev/rules.d/80-nvidia-pm.rules'

UDEV_PM = '''# Automatically generated by EnvyControl

# Remove NVIDIA USB xHCI Host Controller devices, if present
ACTION=="add", SUBSYSTEM=="pci", ATTR{vendor}=="0x10de", ATTR{class}=="0x0c0330", ATTR{remove}="1"

# Remove NVIDIA USB Type-C UCSI devices, if present
ACTION=="add", SUBSYSTEM=="pci", ATTR{vendor}=="0x10de", ATTR{class}=="0x0c8000", ATTR{remove}="1"

# Remove NVIDIA Audio devices, if present
ACTION=="add", SUBSYSTEM=="pci", ATTR{vendor}=="0x10de", ATTR{class}=="0x040300", ATTR{remove}="1"

# Enable runtime PM for NVIDIA VGA/3D controller devices on driver bind
ACTION=="bind", SUBSYSTEM=="pci", ATTR{vendor}=="0x10de", ATTR{class}=="0x030000", TEST=="power/control", ATTR{power/control}="auto"
ACTION=="bind", SUBSYSTEM=="pci", ATTR{vendor}=="0x10de", ATTR{class}=="0x030200", TEST=="power/control", ATTR{power/control}="auto"

# Disable runtime PM for NVIDIA VGA/3D controller devices on driver unbind
ACTION=="unbind", SUBSYSTEM=="pci", ATTR{vendor}=="0x10de", ATTR{class}=="0x030000", TEST=="power/control", ATTR{power/control}="on"
ACTION=="unbind", SUBSYSTEM=="pci", ATTR{vendor}=="0x10de", ATTR{class}=="0x030200", TEST=="power/control", ATTR{power/control}="on"
'''

XORG_PATH = '/etc/X11/xorg.conf'

XORG_INTEL = '''# Automatically generated by EnvyControl

Section "ServerLayout"
    Identifier "layout"
    Screen 0 "nvidia"
    Inactive "intel"
EndSection

Section "Device"
    Identifier "nvidia"
    Driver "nvidia"
    BusID "PCI:{}"
EndSection

Section "Screen"
    Identifier "nvidia"
    Device "nvidia"
    Option "AllowEmptyInitialConfiguration"
EndSection

Section "Device"
    Identifier "intel"
    Driver "modesetting"
EndSection

Section "Screen"
    Identifier "intel"
    Device "intel"
EndSection
'''

XORG_AMD = '''# Automatically generated by EnvyControl

Section "ServerLayout"
    Identifier "layout"
    Screen 0 "nvidia"
    Inactive "amdgpu"
EndSection

Section "Device"
    Identifier "nvidia"
    Driver "nvidia"
    BusID "PCI:{}"
EndSection

Section "Screen"
    Identifier "nvidia"
    Device "nvidia"
    Option "AllowEmptyInitialConfiguration"
EndSection

Section "Device"
    Identifier "amdgpu"
    Driver "amdgpu"
EndSection

Section "Screen"
    Identifier "amd"
    Device "amdgpu"
EndSection
'''

EXTRA_PATH = '/etc/X11/xorg.conf.d/10-nvidia.conf'

EXTRA_CONTENT = '''# Automatically generated by EnvyControl

Section "OutputClass"
    Identifier "nvidia"
    MatchDriver "nvidia-drm"
    Driver "nvidia"
'''

TEARING_FIX = f'    Option "ForceCompositionPipeline" "true"\n'

COOLBITS = f'    Option "Coolbits" "28"\n'

MODESET_PATH = '/etc/modprobe.d/nvidia.conf'

MODESET_CONTENT = '''# Automatically generated by EnvyControl

options nvidia-drm modeset=1
options nvidia NVreg_PreserveVideoMemoryAllocations=1
'''

MODESET_PM = '''# Automatically generated by EnvyControl

options nvidia-drm modeset=1
options nvidia "NVreg_DynamicPowerManagement=0x02"
options nvidia NVreg_PreserveVideoMemoryAllocations=1
'''

SDDM_XSETUP_PATH = '/usr/share/sddm/scripts/Xsetup'

SDDM_XSETUP_CONTENT = '''#!/bin/sh
# Xsetup - run as root before the login dialog appears

'''

LIGHTDM_SCRIPT_PATH = '/etc/lightdm/nvidia.sh'

LIGHTDM_CONFIG_PATH = '/etc/lightdm/lightdm.conf.d/20-nvidia.conf'

LIGHTDM_CONFIG_CONTENT = '''# Automatically generated by EnvyControl

[Seat:*]
display-setup-script=/etc/lightdm/nvidia.sh
'''

NVIDIA_XRANDR_SCRIPT = '''#!/bin/sh
# Automatically generated by EnvyControl

xrandr --setprovideroutputsource "{}" NVIDIA-0
xrandr --auto
'''

def switcher(mode, display_manager = ''):
    _check_root()
    yes = ('yes', 'y', 'ye','evet')
    if mode == 'integrated':
        _cleanup()
        try:
            # Blacklist all nouveau and Nvidia modules
            _create_file(BLACKLIST_PATH, BLACKLIST_CONTENT)
            # Power off the Nvidia GPU with udev rules
            _create_file(UDEV_INTEGRATED_PATH, UDEV_INTEGRATED)
        except Exception as e:
            fonksiyonlar.uyari(f'Hata: {e}')
            sys.exit(1)
        _rebuild_initramfs()
    elif mode == 'hybrid':
        _cleanup()
        # Enable modeset for Nvidia driver
        choice = fonksiyonlar.sorgu("RTD3 güç yönetcisi etkinleştirilsin mi?")
        if choice in yes:
            _create_file(UDEV_PM_PATH, UDEV_PM)
            _create_file(MODESET_PATH, MODESET_PM)
        else:
            _create_file(MODESET_PATH, MODESET_CONTENT)
        _rebuild_initramfs()
    elif mode == 'nvidia':
        _cleanup()
        # detect if Intel or AMD iGPU
        igpu_vendor = _get_igpu_vendor()
        # get the Nvidia dGPU PCI bus
        pci_bus = _get_pci_bus()
        # get display manager
        if display_manager == '':
            display_manager = check_display_manager()
        try:
            # Create X.org config
            if igpu_vendor == 'intel':
                _create_file(XORG_PATH, XORG_INTEL.format(pci_bus))
                _setup_display_manager(display_manager)
            elif igpu_vendor == 'amd':
                _create_file(XORG_PATH, XORG_AMD.format(pci_bus))
                _setup_display_manager(display_manager)
            # Enable modeset for Nvidia driver
            _create_file(MODESET_PATH, MODESET_CONTENT)
            choice = fonksiyonlar.sorgu("Kompozisyon ardışık düzenini zorla etkinleştirilsin mi(ForceCompositionPipeline)?")
            if choice in yes:
                enable_comp = True
            else:
                enable_comp = False
            choice = fonksiyonlar.sorgu("Coolbit etkinleştirilsin mi?")
            if choice in yes:
                enable_coolbits = True
            else:
                enable_coolbits = False
            if enable_comp and enable_coolbits:
                _create_file(EXTRA_PATH,EXTRA_CONTENT+TEARING_FIX+COOLBITS+'EndSection')
            elif enable_comp:
                _create_file(EXTRA_PATH,EXTRA_CONTENT+TEARING_FIX+'EndSection')
            elif enable_coolbits:
                _create_file(EXTRA_PATH,EXTRA_CONTENT+COOLBITS+'EndSection')
        except Exception as e:
            fonksiyonlar.uyari(f'Hata: {e}')
            sys.exit(1)
        _rebuild_initramfs()
    else:
        fonksiyonlar.uyari('Hata: sağlanan grafik modu geçerli değil')
        fonksiyonlar.uyari('Desteklenen grafik modu: entege, nvidia, ikili')
        sys.exit(1)
    fonksiyonlar.uyari(f'Grafik modu {mode} ayarlandı\nLütfen etkinleştirmek için yeniden başlatın!')
    exit(1)

def _cleanup():
    # Remove all files created by EnvyControl
    to_remove = (BLACKLIST_PATH,UDEV_INTEGRATED_PATH, UDEV_PM_PATH, XORG_PATH, EXTRA_PATH, '/etc/X11/xorg.conf.d/90-nvidia.conf', MODESET_PATH, LIGHTDM_SCRIPT_PATH, LIGHTDM_CONFIG_PATH)
    for file in to_remove:
        try:
            os.remove(file)
        except OSError as e:
            if e.errno != 2:
                fonksiyonlar.uyari(f'Hata: {e}')
                sys.exit(1)
    # restore Xsetup backup if found
    if os.path.exists(SDDM_XSETUP_PATH+'.bak'):
            with open(SDDM_XSETUP_PATH+'.bak', mode='r', encoding='utf-8') as f:
                _create_file(SDDM_XSETUP_PATH, f.read())

def _get_igpu_vendor():
    pattern_intel = re.compile(r'(VGA).*(Intel)')
    pattern_amd = re.compile(r'(VGA).*(ATI|AMD|AMD\/ATI)')
    lspci = subprocess.run(['lspci'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    if pattern_intel.findall(lspci):
        return 'intel'
    elif pattern_amd.findall(lspci):
        return 'amd'
    else:
        fonksiyonlar.uyari('Hata: Intel or AMD iGPU bulunamıyor')
        sys.exit(1)

def _get_amd_igpu_name():    
    pattern = re.compile(r'(name:).*(ATI*|AMD*|AMD\/ATI)*')
    xrandr = subprocess.run(['xrandr', '--listproviders'], capture_output=True, text=True).stdout

    if pattern.findall(xrandr):
        name = re.search(pattern, xrandr).group(0)[5:]
    else:
        name = "Error: could not find AMD iGPU"
    return name

def _get_pci_bus():
    pattern = re.compile(
        r'([0-9a-f]{2}:[0-9a-z]{2}.[0-9]).*(VGA compatible controller: NVIDIA|3D controller: NVIDIA)')
    lspci = subprocess.run(['lspci'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    try:
        # Need to return Bus ID in PCI:X:X:X format
        return ':'.join([str(int(element, 16)) for element in pattern.findall(lspci)[0][0].replace('.', ':').split(':')])
    except Exception:
        fonksiyonlar.uyari(f'Hata: doğrudan tümleşik moddan Nvidia moduna geçiş desteklenmez\nİlk olarak ikili moda geçiniz!')
        sys.exit(1)

def check_display_manager():
    # automatically detect the current Display Manager
    # this depends on systemd
    pattern = re.compile(r'(\/usr\/bin\/|\/usr\/sbin\/)(.*)')
    try:
        with open('/etc/systemd/system/display-manager.service',mode='r', encoding='utf-8') as f:
            display_manager = pattern.findall(f.read())[0][1]
    except Exception:
        display_manager = ''
        fonksiyonlar.uyari('Uyarı: Otomatik görüntü yönetci bulunamdı')
    finally:
        return display_manager

def _setup_display_manager(display_manager):
    # setup the Xrandr script if necessary
    # get igpu vendor to use if needed
    igpu_vendor = _get_igpu_vendor()
    if display_manager == 'sddm':
        # backup Xsetup
        if os.path.exists(SDDM_XSETUP_PATH):
            with open(SDDM_XSETUP_PATH, mode='r', encoding='utf-8') as f:
                _create_file(SDDM_XSETUP_PATH+'.bak', f.read())
        if igpu_vendor == "intel":
            _create_file(SDDM_XSETUP_PATH, NVIDIA_XRANDR_SCRIPT.format("modesetting"))
        else:
            amd_name = _get_amd_igpu_name()
            _create_file(SDDM_XSETUP_PATH, NVIDIA_XRANDR_SCRIPT.format(amd_name))
        subprocess.run(['chmod','+x',SDDM_XSETUP_PATH], stdout=subprocess.DEVNULL)
    elif display_manager == 'lightdm':
        if igpu_vendor == "amd":
            amd_name = _get_amd_igpu_name()
            _create_file(LIGHTDM_SCRIPT_PATH, NVIDIA_XRANDR_SCRIPT.format(amd_name))
        else:
            _create_file(LIGHTDM_SCRIPT_PATH, NVIDIA_XRANDR_SCRIPT.format("modesetting"))
        subprocess.run(['chmod','+x',LIGHTDM_SCRIPT_PATH], stdout=subprocess.DEVNULL)
        # create config
        if not os.path.exists(os.path.dirname(LIGHTDM_CONFIG_PATH)):
            _create_file(LIGHTDM_CONFIG_PATH, LIGHTDM_CONFIG_CONTENT)
    elif display_manager not in ['', 'gdm', 'gdm3']:
        fonksiyonlar.uyari('Hata: Sağlanan Görüntü Yöneticisi geçerli değil')
        fonksiyonlar.uyari('desteklene görüntü yöneticisi: gdm, sddm, lightdm')
        sys.exit(1)

def _rebuild_initramfs():
    # Debian and Ubuntu derivatives
    if os.path.exists('/etc/debian_version'):
        command = ['update-initramfs', '-u', '-k', 'all']
    # RHEL and SUSE derivatives
    elif os.path.exists('/etc/redhat-release') or os.path.exists('/usr/bin/zypper'):
        command = ['dracut', '--force', '--regenerate-all']
    else:
        command = []
    if len(command) != 0:
        fonksiyonlar.uyari('Rebuilding initramfs...')
        p = subprocess.run(command, stdout=subprocess.DEVNULL)
        if p.returncode == 0:
            fonksiyonlar.uyari('initramfs inşası başarılı!')
        else:
            fonksiyonlar.uyari('Hata: initramfs yeniden oluşturulurken bir hata oluştu')

def _check_root():
    if not os.geteuid() == 0:
        fonksiyonlar.uyari('Hata: bu işlem kök(root) yetkisi gerektirir')
        sys.exit(1)

def _create_file(path, content):
    # Create parent folders if needed
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    with open(path, mode='w', encoding='utf-8') as f:
        f.write(content)

def _query_mode():
    if os.path.exists(BLACKLIST_PATH) and os.path.exists(UDEV_INTEGRATED_PATH):
        mode = 'integrated'
    elif os.path.exists(XORG_PATH) and os.path.exists(MODESET_PATH):
        mode = 'nvidia'
    else:
        mode = 'hybrid'
    fonksiyonlar.uyari(f'şu anki grafik modu: {mode}')

def _reset_sddm():
    _check_root()
    try:
        _create_file(SDDM_XSETUP_PATH, SDDM_XSETUP_CONTENT)
        subprocess.run(['chmod', '+x', SDDM_XSETUP_PATH], stdout=subprocess.DEVNULL)
    except Exception as e:
        fonksiyonlar.uyari(f'Hata: {e}')
        sys.exit(1)
    fonksiyonlar.uyari('İşlem başarıyla tamamlandı!')

def _print_version():
    fonksiyonlar.uyari(f'EnvyControl sürümü {VERSION}')

def main():
    # argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--version', action='store_true', help='show this program\'s version number and exit')
    parser.add_argument('-s', '--switch', type=str, metavar='MODE', action='store', help='switch the graphics mode, supported modes: integrated, hybrid, nvidia')
    parser.add_argument('-q', '--query', action='store_true', help='query the current graphics mode set by EnvyControl')
    parser.add_argument('--dm', type=str, metavar='DISPLAY_MANAGER', action='store',
                        help='Manually specify your Display Manager. This is required only for systems without systemd. Supported DMs: gdm, sddm, lightdm')
    parser.add_argument('--reset', action='store_true', help='remove EnvyControl settings')
    parser.add_argument('--reset-sddm', action='store_true', help='restore original SDDM Xsetup file')
    # print help if no arg is provided
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()
    if args.query:
        _query_mode()
    elif args.version:
        _print_version()
    elif args.reset:
        _cleanup()
    elif args.reset_sddm:
        _reset_sddm()
    elif args.switch:
        if args.dm and args.switch == 'nvidia':
            switcher(args.switch, args.dm)
        else:
            switcher(args.switch)
    elif args.dm and not args.switch:
        fonksiyonlar.uyari('Hata: bu seçeneğin --switch nvidia ile kullanılması amaçlanmıştır')
        fonksiyonlar.uyari('Örneğin: sudo envycontrol --switch nvidia --dm sddm')
        sys.exit(1)

if __name__ == '__main__':
    main()
