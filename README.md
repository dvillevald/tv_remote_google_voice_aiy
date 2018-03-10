# WORK IN PROGRESS
## Motivation

Replace old TV/Roku remotes with voice-controlled Google Voice AIY kit using Google Assistant Library

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

Schematics of Voice Hat connections             | Soldered wires to Voice Hat
:----------------------------------------------:|:------------------------------------------------------------:
<img src="https://github.com/dvillevald/tv_remote_google_voice_aiy/blob/master/images/Voice_HAT_Hardware_Extensions.png" width="425"/>    |  <img src="https://github.com/dvillevald/tv_remote_google_voice_aiy/blob/master/images/Soldering_cables_to_HAT_board.JPG" width="425"/>

### 2. Assemble hardware with IR components. Solder JST connector, IR LED, IR receiver, resistors and transistor to a circuit board

<img src="https://github.com/dvillevald/tv_remote_google_voice_aiy/blob/master/images/Schematics.jpg" width="425"/> 

Front                                           | Back
:----------------------------------------------:|:------------------------------------------------------------:
<img src="https://github.com/dvillevald/tv_remote_google_voice_aiy/blob/master/images/Voice_HAT_Hardware_Extensions.png" width="425"/>    |  <img src="https://github.com/dvillevald/tv_remote_google_voice_aiy/blob/master/images/Soldering%20cables%20to%20HAT%20board%20.JPG" width="425"/>


The completed circuit board:

![Schematics of IR hardware extension](https://github.com/dvillevald/tv_remote_google_voice_aiy/blob/master/images/RPI1_schem.jpg)


### 3. Assemble Google Voice AIY kit

Follow instructions at (https://aiyprojects.withgoogle.com/voice) and assemble Google Voice AIY kit. 


### Assemble hardware

Follow instructions at (https://aiyprojects.withgoogle.com/voice) and assemble Google Voice AIY kit. 




## Software
- LIRC package to detect and send infrared (IR) signals
- Python script 

## Assemble hardware

Follow instructions at (https://aiyprojects.withgoogle.com/voice) and assemble Google Voice AIY kit. 
