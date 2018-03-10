# WORK IN PROGRESS
## Motivation

Replace old TV/Roku remotes with voice-controlled Google Voice AIY kit using Google Assistant Library

## Software
- LIRC package to detect and send infrared (IR) signals
- Python script 

## Hardware
- Google Voice AIY kit (http://www.microcenter.com/product/483414/AIY_Voice_Kit)
- Raspberry PI 3 Model B
- Power supply for Raspberry PI
- Infrared LED and receiver (https://www.amazon.com/gp/product/B00EFOTJZE/ref=pe_62860_272369200_em_1p_0_ti)
- Resistors 68 Ohm and 1 kOhm
- Transistor P2N2222 (or similar transistor)
- Circuit board (2cm x 8cm)
- 4-pin JST-XH Connector Pair
- 2-sided sticky foam tape

<img src="https://github.com/dvillevald/tv_remote_google_voice_aiy/blob/master/images/Hardware_components.jpg" width="425"/>

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

### 5. Download and install LIRC software

There are several very good tutorials on how to install LIRC on Raspberry PI. For example, you can follow the one from [Austin Stanton](https://www.hackster.io/austin-stanton/creating-a-raspberry-pi-universal-remote-with-lirc-2fd581). **Make sure you reference the right pins - unlike Austin's tutorial we use output pin 26 and input pin 24 here.** 

- Install LIRC

```
$ sudo apt-get install lirc
```

- Add to your /etc/modules file by entering the command below

```
$ sudo cat >> /etc/modules <<EOF
lirc_dev
lirc_rpi gpio_in_pin=24 gpio_out_pin=26
EOF
```

- Change your /etc/lirc/hardware.conf file by entering the command below

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
- Edit your /boot/config.txt by entering the command below

```
$ cat >> /boot/config.txt <<EOF
dtoverlay=lirc-rpi,gpio_in_pin=24,gpio_out_pin=26
EOF 
```
- Now restart lircd so it picks up these changes:

```
$ sudo /etc/init.d/lirc stop
$ sudo /etc/init.d/lirc start
```

- Testing the IR receiver. Run these two commands to stop lircd and start outputting raw data from the IR receiver:

```
$ sudo /etc/init.d/lirc stop
$ mode2 -d /dev/lirc0
```

- Point a remote control at your IR receiver and press some buttons. You should see something like this:

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

- Testing the IR LED. You’re going to need to either find an existing LIRC config file for your remote control or use your IR receiver to generate a new LIRC config file (find existing remote profiles [here](http://lirc.sourceforge.net/remotes/)). In my case, I created a new LIRC config file. To do this, read the documentation on the [irrecord](http://www.lirc.org/html/irrecord.html). application that comes with LIRC. When using irrecord it will ask you to name the buttons you’re programming as you program them. Be sure to run `irrecord --list-namespace` to see the valid names before you begin. 

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

You can use two or more remote controls (I used two - TV and Roku) with *irrecord*. In my case TV remote generated a single command (e.g. 0x42BD807F) while Roku - two (e.g. 0x5743C03F 0x5743C13E.) You can find my lircd.conf file [here]()    

- Once you’ve completed a remote configuration file and saved/added it to */etc/lirc/lircd.conf* you can try testing the IR LED. We’ll be using the [irsend](http://www.lirc.org/html/irsend.html) application that comes with LIRC to facilitate sending commands from command line. You’ll definitely want to check out the documentation to learn more about the options irsend has.

Here are the commands I ran to test my IR LED (using the “/home/pi/lircd.conf” remote configuration file I created):

```
# List all of the commands that LIRC knows for 'Roku'
$ irsend LIST /home/pi/lircd.conf ""

# Send the KEY_POWER command once
$ irsend SEND_ONCE /home/pi/lircd.conf KEY_POWER
```
You can test that it is was working by pointing the IR LED at your TV/Roku and testing whether you could turn it on (I am assuming you programmed KEY_POWER to turn on your TV). Another way to test is to use your cellphone camera to see if LED blinks when you send commands with *irsend*. It did not work with my iPhone but worked fine with Android phone (Samsung Galaxy.)





