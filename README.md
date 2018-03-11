## Motivation

Replace old TV/Roku remotes with voice-controlled Google Voice AIY kit using Google Assistant Library

## Software
- LIRC package to detect and send infrared (IR) signals
- Python [script](https://github.com/dvillevald/tv_remote_google_voice_aiy/blob/master/code/ir_remote_assistant_library.py) 

## Hardware
- Google Voice AIY kit available [here](http://www.microcenter.com/product/483414/AIY_Voice_Kit)
- Raspberry PI 3 Model B
- Power supply for Raspberry PI
- Infrared LED and receiver (I purchased them [here](https://www.amazon.com/gp/product/B00EFOTJZE/ref=pe_62860_272369200_em_1p_0_ti))
- Resistors 68 Ohm and 1 kOhm
- Transistor P2N2222 (or similar transistor)
- Circuit board (2cm x 8cm)
- 4-pin JST-XH Connector Pair
- 2-sided sticky foam tape

<img src="https://github.com/dvillevald/tv_remote_google_voice_aiy/blob/master/images/Hardware_components.jpg" width="425"/>

## Warning

I strongly recommend to test this project on a breadboard first before starting soldering.  

## Project steps

### 1. Solder wires of 4-pin JST-XH Connector to GPIO pins 24, 26, GND and 5V of Voice HAT (marked by red rectangulars below)

- White wire should be connected to IR LED
- Yellow - to IR receiver
- Red - to 5V
- Black - to GND.

Schematics of Voice Hat connections             | Soldered wires to Voice Hat
:----------------------------------------------:|:------------------------------------------------------------:
<img src="https://github.com/dvillevald/tv_remote_google_voice_aiy/blob/master/images/Voice_HAT_Hardware_Extensions.png" width="425"/>    |  <img src="https://github.com/dvillevald/tv_remote_google_voice_aiy/blob/master/images/Soldering_cables_to_HAT_board.JPG" width="425"/>

### 2. Assemble hardware with IR components. Solder JST connector, IR LED, IR receiver, resistors and transistor to a circuit board

<img src="https://github.com/dvillevald/tv_remote_google_voice_aiy/blob/master/images/IR_block_schematics.png" width="425"/> 

If you use a different transistor, check its pinout in the datasheet. For example, pinouts of P2N2222 and PN2222 are different.

The assembled IR block:

Front                                           | Back
:----------------------------------------------:|:------------------------------------------------------------:
<img src="https://github.com/dvillevald/tv_remote_google_voice_aiy/blob/master/images/Front.JPG" width="425"/>    |  <img src="https://github.com/dvillevald/tv_remote_google_voice_aiy/blob/master/images/Rear.JPG" width="425"/>

### 3. Assemble Google Voice AIY kit

Follow instructions at (https://aiyprojects.withgoogle.com/voice) and assemble Google Voice AIY kit. 

### 4. Connect IR block to Google Voice AIY kit

Make an opening in the wall of the carton box for IR LED and receiver and attached the IR circuit board to the wall with 2-sided sticky foam tape.

<img src="https://github.com/dvillevald/tv_remote_google_voice_aiy/blob/master/images/Hardware_to_assemble.jpg" width="425" height="425"/>    |   <img src="https://github.com/dvillevald/tv_remote_google_voice_aiy/blob/master/images/Hardware_with_sticky_tape.JPG" width="425" height="425"/>

<img src="https://github.com/dvillevald/tv_remote_google_voice_aiy/blob/master/images/Assembled_box.JPG" width="425" height="425"/> |
<img src="https://github.com/dvillevald/tv_remote_google_voice_aiy/blob/master/images/Fully_assembled_device2.JPG" width="425" height="425"/>

### 5. Download, install and configure LIRC software

There are several very good tutorials on how to install LIRC on Raspberry PI. Here I follow the one created by [Austin Stanton](https://www.hackster.io/austin-stanton/creating-a-raspberry-pi-universal-remote-with-lirc-2fd581). **If you are using Austin's tutorial, make sure you reference the right pins - unlike Austin's tutorial I use output pin 26 and input pin 24 here. Also, unlike Astin who used the name "Roku" in lircd.conf file for his remote configuration, I am using the name “/home/pi/lircd.conf”.** 

Install LIRC on Raspberry PI of your device

```
$ sudo apt-get install lirc
```

Add to your `/etc/modules` file by entering the command below

```
$ sudo cat >> /etc/modules <<EOF
lirc_dev
lirc_rpi gpio_in_pin=24 gpio_out_pin=26
EOF
```

Change your /etc/lirc/hardware.conf file by entering the command below

```
$ sudo cat > /etc/lirc/hardware.conf <<EOF 
########################################################
# /etc/lirc/hardware.conf
#
# Arguments which will be used when launching lircd
LIRCD_ARGS="--uinput"
# Don't start lircmd even if there seems to be a good config file
# START_LIRCMD=false
# Don't start irexec, even if a good config file seems to exist.
# START_IREXEC=false
# Try to load appropriate kernel modules
LOAD_MODULES=true
# Run "lircd --driver=help" for a list of supported drivers.
DRIVER="default"
# usually /dev/lirc0 is the correct setting for systems using udev
DEVICE="/dev/lirc0"
MODULES="lirc_rpi"
# Default configuration files for your hardware if any
LIRCD_CONF=""
LIRCMD_CONF=""
######################################################## 
EOF
```
Edit your /boot/config.txt:

```
$ cat >> /boot/config.txt <<EOF
dtoverlay=lirc-rpi,gpio_in_pin=24,gpio_out_pin=26
EOF 
```
Now restart lircd so it picks up these changes:

```
$ sudo /etc/init.d/lirc stop
$ sudo /etc/init.d/lirc start
```

Testing the IR receiver. Run these two commands to stop lircd and start outputting raw data from the IR receiver:

```
$ sudo /etc/init.d/lirc stop
$ mode2 -d /dev/lirc0
```

Point a remote control at your IR receiver and press some buttons. You should see something like this:

```
space 16300
pulse 95
space 28794
pulse 80
space 19395
pulse 83
space 402351
pulse 135
space 7085
pulse 85
space 2903
```

### 6. Create LIRC remote configuration file. 

You’re going to need to either find an existing LIRC config file for your remote control or use your IR receiver to generate a new LIRC config file (find existing remote profiles [here](http://lirc.sourceforge.net/remotes/)). In my case, I created a new LIRC config file. To do this, read the documentation on the [irrecord](http://www.lirc.org/html/irrecord.html) application that comes with LIRC. When using `irrecord` it will ask you to name the buttons you’re programming as you program them. It helps to run `irrecord --list-namespace` before you begin to see the valid names. You can use one, two or more remote control (I used two - one for TV and another for Roku player) with `irrecord`. I suggest to select the button names which make it easy to understand what actions they relate to (KEY_POWER for turning on/off the TV, etc.) 

Here were the commands that I ran to generate a remote configuration file:

```
# Stop lirc to free up /dev/lirc0
$ sudo /etc/init.d/lirc stop

# Create a new remote control configuration file (using /dev/lirc0) and save the output to ~/lircd.conf
$ irrecord -d /dev/lirc0 ~/lircd.conf

# Make a backup of the original lircd.conf file
$ sudo mv /etc/lirc/lircd.conf /etc/lirc/lircd_original.conf

# Copy over your new configuration file
$ sudo cp ~/lircd.conf /etc/lirc/lircd.conf

# Start up lirc again
$ sudo /etc/init.d/lirc start
```

After this step your config file `/etc/lirc/lircd.conf` should look similar to [mine](https://github.com/dvillevald/tv_remote_google_voice_aiy/blob/master/code/lircd.conf). You can see that my TV remote sends a single IR command (e.g. KEY_POWER 0x42BD807F) while Roku sends two (e.g. KEY_HOME 0x5743C03F 0x5743C13E.) Note that the name of my remote configuration (referenced in line of config file starting with "name") is "/home/pi/lircd.conf" while Austin uses name "Roku" in his tutorial. 

### 7. Test IR LED. 

Once you’ve completed a remote configuration file and saved/added it to */etc/lirc/lircd.conf* you are ready to test IR LED. We’ll be using the [irsend](http://www.lirc.org/html/irsend.html) application that comes with LIRC to facilitate sending commands from command line. You’ll want to check out the documentation to learn more about the options `irsend` has.

The command `irsend` uses the name of your remote configuration (I am using the name “/home/pi/lircd.conf”; you can find yours in your config file `/etc/lirc/lircd.conf` in the line which starts with "name"):

```
# List all of the commands that LIRC knows for '/home/pi/lircd.conf'
$ irsend LIST /home/pi/lircd.conf ""

# Send the KEY_POWER command once
$ irsend SEND_ONCE /home/pi/lircd.conf KEY_POWER
```
You can test if it is working by pointing the IR LED at your TV and testing whether you could turn it on (I am assuming you programmed KEY_POWER to turn on your TV). Another way to test is to use your cellphone camera to see if LED blinks when you send commands with `irsend`. I could not see LED blinking on my iPhone camera but it worked fine with Android phone (Samsung Galaxy.)

### 8. Sign in to the Google Cloud Platform

Use your Google account to sign in to the Google Cloud Platform (GCP). If you don't have one you will have to create one. This project uses Google Assistant API which is free to personal use at the moment of writing and let you make 500 calls per day. Google explains how to setup your account, create credentials and sign in to the GCP [here](https://aiyprojects.withgoogle.com/voice#users-guide). Make sure you enable **Google Assistant API.**

### 9. Test the device

The Python script [ir_remote_assistant_library.py](https://github.com/dvillevald/tv_remote_google_voice_aiy/blob/master/code/ir_remote_assistant_library.py) used for this project is a modified version of `/AIY-voice-kit-python/src/assistant_library_demo.py`. **Warning: the folder names and folder structure on your Raspberry Pi may be different from the ones on the [Google's Voice kit website](https://aiyprojects.withgoogle.com/voice#makers-guide) so make sure to check your folder names and paths.** 

I strongly recommend to check Google Assistant Library [documentation](https://developers.google.com/assistant/sdk/reference/library/python/) for details on lifecycle handling for the Google Assistant and explanation of stream of Events relaying the various Assistant states. 

Copy `ir_remote_assistant_library.py` into the folder `/AIY-voice-kit-python/src`.

Open the script `/AIY-voice-kit-python/src/ir_remote_assistant_library.py` with the text editor or IDE. Open your lirc config file `/etc/lirc/lircd.conf` with text editor. Make sure that (1) the values of `voice_command_to_key` discionary in the Python script (KEY_POWER, etc.) match the ones from config file and (2) the value of `remote_name` variable (I used '/home/pi/lircd.conf') in the Python script matches the configuration name (you can find it in line which starts with "name") of your lirc config file.   

Open development terminal on Raspberry Pi of your device:

<img src="https://github.com/dvillevald/tv_remote_google_voice_aiy/blob/master/images/Start_dev_terminal.png" width="425"/>

Run the script

```
(env) py@raspberrypi:~/AIY-voice-kit-python $ src/ir_remote_assistant_library.py
```

In addition to using Google Voice AIY kit as your voice-controlled TV remote, the script also allows you to fully utilize Google Assistant API (asking questions about weather, time, traffic, etc.) Every time you say "Hey Google" or "OK Google", the script listens to your voice request which follows and then sends this request to Google Assistant API which returns back a text string (your request) which can be used to control your TV or other applicances and a voice message from Assistant with information your requested. This device can be used in two modes:

- **Assistant + Remote Control Mode**. If you say **"Hey Google, I need your help"** then you should hear a response "I am listening" and Google Asistant will turn into "Assistant mode" responding to your requests (don't forget to say "Hey Google" before each request) with voice messages. It will also continue working as your TV remote sending IR signals based on your voice commands.

- **Remote Control Only Mode**. If you only want use this device as a TV remote then say **"Hey Google, get some rest"**. You will hear a confirmation "Let me know when you need my help" and Google Assistant will stop engaging into conversation (i.e. ignore your questions about weather, etc.) and only serve as a remote control. You can always activate "Assistant + Remote Control Mode" again by saying "Hey Google, I need your help".  

Hints:

- Make sure that bright LED inside the arcade button mounted on top of the device is ON before you proceed with a voice command. This means the device is listening.
- Point infrared LED toward your TV and make sure it is not too far so the signal is strong enough. If remote commands are not working, check if your IR LED sends a signal (with your cellphone camera.)
- Make sure the room is not too noisy so the Assistant can understand your voice commands. Move closer to the device if it is.
- Remember your voice commands. Your device will understanf "Turn on TV", for example, but will do nothing if you say "Turn TV on".
- Control your quota - you can only make 500 requests per day. You can check your usage by navigatinng to 
  - [Google Cloud platform](https://console.cloud.google.com),
  - Selecting **APIs & Services -> Dashboard** from the dropdown menu in the upper left corner,
  - Clicking on **Google Assistant API** in the API list, and
  - Clicking on **Quotas** on the page that will open.
You screen should show a bar chart with your daily usage:
  
<img src="https://github.com/dvillevald/tv_remote_google_voice_aiy/blob/master/images/Quotas.png"/>
  
### 10. Automate the process
Once you the script is working, it is time to automate the process. 

### Shutdown

The shutdown is already implemented in the code. You have to say "Hey Google" and then **"Google shut down."** The device will respond saying "Shutting down" and shut down. Note that there are two "Googles" here - one from hotword ("Hey Google") and another - from the voice command ("Google shut down".) This is done on purpose to avoid device's shut down by accident. 

### Launching app on startup

Google [explains](https://aiyprojects.withgoogle.com/voice#makers-guide) in section **RUN YOUR APP AUTOMATICALLY** how to setup and activate the system service which will start your application when Raspberry PI starts:

- Open text editor, type the following. **Make sure that the folder names match the ones on your Raspberry Pi!**:
```
Description=My awesome assistant app

[Service]
ExecStart=/bin/bash -c '/home/pi/AIY-voice-kit-python/env/bin/python3 -u src/ir_remote_assistant_library.py'
WorkingDirectory=/home/pi/AIY-voice-kit-python
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
```
- Save the result as `ir_remote_assistant_library.service`
- Move the created file into system folder:
```
$ sudo mv ir_remote_assistant_library.service /lib/systemd/system/
```
- Now your service has been configured! To enable your service, enter the following command (note that we are referring to the service, not the name of Python script it runs):
```
$ sudo systemctl enable ir_remote_assistant_library.service
```

To manually start your service, enter:
```
$ sudo service ir_remote_assistant_library start
```

To monitor your service status (very useful for debugging), enter:
```
$ sudo service ir_remote_assistant_library status -l
```
**That is it!**

Finally, if you want to manually stop your service, enter
```
$ sudo service ir_remote_assistant_library stop
```
To disable your service, enter:
```
$ sudo systemctl disable ir_remote_assistant_library.service
```

### Device in action

<a href="https://youtu.be/X5MmewNA6f4" target="_blank"><img src="https://github.com/dvillevald/tv_remote_google_voice_aiy/blob/master/images/Youtube.png" 
alt="Google Voice AIY with added TV remote functionality in action" width="480" height="360" border="10" /></a>

### Final thoughts
- On some occasions the remote voice command is executed properly (i.e. sends the correct IR signal to the TV) but triggers a message `ALSA lib pcm.c:7843:(snd_pcm_recover) overrun occurred`. Despite my efforts I was unable to fully understand why this happens and fix this issue.

- Sometimes, usually after a long period with no activity, I was getting a voice response **"Hmm, something went wrong. Try again in a few seconds"** When this happens the service should restart and the same request sends seconds later was usually processed with no issues.  

- It is a bit annoying to say a hotword "Hey Google" mupltiple times when you are trying to navigate to the movie you would like to watch through the grid on Netflix or Amazon Prime. Clicking arcade button mounted on top of the device instead is an option but it denies the purpose of the remote. Making Google constantly listening to your conversation until you say something like "Google turn on TV" is possible with a Google Cloud API but would be prohibitively expensive. A better alternative would be to use a different activation trigger like motion detector or via computer vision application (detection of raised arm, for example.)

- When you are navigating through the grid of movies on Netflix or Amazon Prime, one way to increase efficiency would be to combine several remote commands into one so, for example, instead of saying three times "Hey Google, go left" you would say once "Hey Google, go left three steps." It should be easy to implement and this would be a smarter way to use the daily quota.

I hope you enjoyed this tutorial. Let me know if you have comments or questions or if you made a similar project. Thank you!
