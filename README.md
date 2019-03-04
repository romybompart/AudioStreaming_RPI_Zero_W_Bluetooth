# AudioStreaming_RPI_Zero_W_Bluetooth
This is a example project to use the raspberry pi zero w as receiver device of audio via bluetooth

**The hardware required is listed:**
  1. A raspberry pi zero W: https://www.raspberrypi.org/products/raspberry-pi-zero-w/ from @raspberrypi
  2. A hiffiberry Amp2: https://www.hifiberry.com/shop/boards/hifiberry-amp2/ from @hifiberry
  3. Two speakers of 4 ohms and 15W: https://www.amazon.com/gp/product/B01IP390Q8/ref=ppx_yo_dt_b_asin_title_o05_s01?ie=UTF8&psc=1
 
**How configure the raspberry pi zero w to use the hifiberry Amp2 as a sound card:**
  We have follow the steps written by the supplier:https://www.hifiberry.com/build/documentation/configuring-linux-3-18-x/
  1. Let's disable the audio output via hdmi
     In your /boot/config.txt file, comment the line `dtparam=audio=on`, you can use: sudo nano /boot/config.txt to modify the file properly.
  2. Let's set up the correct device tree to access to the hardware
     in the same file ( config.txt ), add a new line code with: `dtoverlay=hifiberry-dacplus`
  3. Save the file by pressing Ctrl + X, Then Y to save the file modification
  
**The next step is optional ( I did):** 
  1. use `sudo nano /etc/asound.conf` and write the following: 
  
  `pcm.hifiberry { type hw card 0}`
  
  `pcm.!default  { type plug
                  slave.pcm "dmixer"}`
  
  `pcm.dmixer  { type dmix
                ipc_key 1024
                slave { pcm "hifiberry"
                        channels 2  }
               }`

   2. Save the file by using Ctrl + X, then Y to apply the changes.
   3. After this please, test it by using the following: aplay -l
   
T**he bluetooth configuration, it was based on the following project:** https://docs.google.com/document/d/12cK4heNd7kY3jYZI_sW1AD407dn_ds-9zZdX4qs-TJg/mobilebasic
 
 1. let's modify the configuration of the bluetooth:
    `sudo nano /etc/bluetooth/main.conf`
 2. That command will open the main.conf file, it will be filled with the default configuration, we are going to add the following line to the [General] section:
    `Enable = Source, Sink, Media, Socket`
 3. That will enable the Raspberry pi zero W as source and sink for audio media. Now Chnage the class to:
    `Class = 0x00041C`
    According to the Bluetooth standard this will change the raspberry pi zero W from default class to Audio/Headphone class.
    A headphone ico will appear when the raspberry pi zero is paired to your device.
  4. Set the values for pairing and discovering times:
    `DiscoverableTimeout= 0`
    `PairableTimeout = 0`
  5. Configure the audio media that will reproduce the sound via the Hifiberry Amp2
     `sudo nano /etc/pulse/daemon.conf`
     when the document is opened, let's change the `resample-method = trivial`
     the method trivial is the most basic algorithm implemented. It is supported by the pi already.
  6. Save the file
  7. Pulseaudio needs to be triggered once, therefore let's write a script to achive this:
     `sudo nano /etc/init.d/pulseaudio.sh`
     And copy the content from the script pulseaudio.sh that is saved in the pulseaudio folder of this repository.
     Paste the content in the file that you just created.     
  8. Save the file and let's make it executable by writting:
        `sudo chmod 755 /etc/init.d/pulseaudio.sh`
  9. Register the script to be run in the startup
        `sudo update-rc.d pulseaudio.sh defaults`
        
 **Now the Bluetooth must be restarted, and we have to make it run:**
  1. `sudo service bluetooth restart`
  2. `bluetoothctl`
  3. `power on`
  4. `show`
      
    At this point you should see a screen like this:
    pi@raspberrypi:~/Documents $ bluetoothctl
    [NEW] Controller B8:27:EB:E4:29:B7 raspberrypi [default]
    [NEW] Device 04:4E:AF:68:91:F7 LG webOS TV
    [NEW] Device AC:07:5F:6A:0A:46 HUAWEI P20
    [NEW] Device A8:B8:6E:AC:E9:0E Q6
    [NEW] Device 80:B0:3D:74:5D:03 iPhone de Santiago
    [bluetooth]# show
    Controller B8:27:EB:E4:29:B7
        Name: raspberrypi
        Alias: raspberrypi
        Class: 0x0c041c
        Powered: yes
        Discoverable: yes
        Pairable: yes
        UUID: PnP Information           (00001200-0000-1000-8000-00805f9b34fb)
        UUID: Generic Access Profile    (00001800-0000-1000-8000-00805f9b34fb)
        UUID: Generic Attribute Profile (00001801-0000-1000-8000-00805f9b34fb)
        UUID: A/V Remote Control        (0000110e-0000-1000-8000-00805f9b34fb)
        UUID: A/V Remote Control Target (0000110c-0000-1000-8000-00805f9b34fb)
        UUID: Audio Source              (0000110a-0000-1000-8000-00805f9b34fb)
        UUID: Audio Sink                (0000110b-0000-1000-8000-00805f9b34fb)
        Modalias: usb:v1D6Bp0246d0517
        Discovering: no
    [bluetooth]#

**Now the raspberry pi zero is ready to go.**
  1. Use your bluetooth device to connect the raspberry pi zero w. I used my smartphone.
         Turn on the bluetooth of your device and look for the raspberry pi zero W. 
         When it is available pair it with your device
  2. You will notice the connection won't be able because the raspberry pi did not register
         your device Bluetooth MAC as trust. So we have to do it manually so far, for example 
         you will have this screen:
         
         [bluetooth]# paired-devices
         Device C0:EE:FB:47:1C:83 HUAWEI P20
         
  3. Next thing to do is to write trust and the MAC Addres like this:
  
          [bluetooth]# trust C0:EE:FB:47:1C:83
       
  4. After that the following messages will appear:
  
          [CHG] Device C0:EE:FB:47:1C:83 Trusted: yes
          Changing C0:EE:FB:47:1C:83 trust succeeded
          [bluetooth]#
          
  5. And nothing else, enjoy playing songs from your device over bluetooth into your raspberry pi zero w.
        
**Now to make this a portable device and not entering in the command prompt all the time to run this.**
Let's make the final setup:
  
  1. sudo raspi-config
       select Boot Option, then go to B2: Console Autologin. Save it
  2. Save in your raspberry pi zero w,  the trust_paired.sh script saved in the bluetooth folder of this repository.
       I recommend to put the script in the following path: /home/pi/
  3. make it executable by using:
       `sudo chmod 755 trust_paired.sh`
  4. let's run the script whenever the pi logs on:
        `sudo nano .bashrc`
        Add the line:
        `/home/pi/trust_paired.sh`
        if you save the script in another path, please use the path name in the .bashrc file
  5. no save and reboot.

**The sound control via python code**
  1. The alsaaudio folder contains a example code to run in the raspberry pi zero W
  2. The code is able to control de volume of the raspberry pi when it is playing the streaming audio.
  3. For android I noticed that the volume buttons from the smartphone can control the volume of the raspberry pi zero W, 
     but the iOS from iphone can't do that, so it will be neccesary to run this code alsaaudio_test.py in order to control
     the audio volume.
  4. run the code in your raspberry pi :
      `sudo python3 alsaaudio_test.py`


**NOTE** 
 When the wifi is enable an audio strutter can be noticed. 
 The only fix for this issue is to turn off the wifi:
 `sudo ifdown wlan0`
   
Romy Bompart
03/04/2019
