# Driver Settings
Since it is difficult for normal users to install some drivers on Linux systems, we tried to simplify this task, insha'Allah.

[Türkçe için](https://github.com/halak0013/Driver-Setting/blob/ana/READMETR.md)
## called and working systems
- kde
- xfce
- gnome

APPLICATION

![resim](https://user-images.githubusercontent.com/75750279/224530171-41b064f2-ed3e-4fde-9a63-f8e851380a7c.png)

## How does it work
        
## the program consists of two parts
1-) installing drivers.

2-) switching to the desired graphic mode.

3-) changing the brightness of the screens (for now, it goes back to when you restart)

## To make it work
- download the program and open the terminal inside the folder
- Run the application with `python3 main.py`.
- press download
- enter the password on the screen
- For sddm press ok and select sddm
- OK if you warn for the latest novue... driver
- then the computer restarts.

## Working principle of the app

### for the loading part
- first the system is updated
- removes troublesome packages
- installs some required packages
- Adds nvidia repository
- the contrib repository is activated
- repository is updated
- Afterwards, according to the selected mode, it is loaded with or without cuda.

### graphics card switch
- If nvida is selected, necessary adjustments are made with envycontrol and only nvidia works.
- if integrated is selected, only the integrated (in-processor) unit is running
- if binary is selected, both nvidia and integrated unit are activated.
     - in this mode, gpu supported programs such as blender and davinci can see nvidia
     - but the rest of the system still works on the integrated unit



graphics card migration done by replacing envycontrol https://github.com/bayasdev/envycontrol



You can choose the mode you want by entering the application again.

* nvidia's own settings

![image](https://user-images.githubusercontent.com/75750279/204157502-05292255-1531-4a23-9de7-61324af6ec66.png)
![image](https://user-images.githubusercontent.com/75750279/219940580-c8e98dbd-774d-4101-b8a4-4a0471052b36.png)


* davinci 18

![image](https://user-images.githubusercontent.com/75750279/204157510-0e4e7794-5c6d-4c06-b658-ad86de31d943.png)

* blender and nvidia-smi

![image](https://user-images.githubusercontent.com/75750279/204157524-af44fa06-ddad-4c72-bd51-03e22a9f4d81.png)

* About Pardus and neofetch

![image](https://user-images.githubusercontent.com/75750279/204157534-4795b2eb-abd4-4ca7-becf-fb048be516f5.png)

# backup alert
!!!!

If you want to install, I highly recommend that you make a backup first. We will try to help if any errors occur, but remember that you are responsible.

!!!

To get a backup, you can download the timeshift program from the store or

```sudo apt install timeshift```


You can install with

If you get any error, share the screenshot in the issue section and I will try to help.
