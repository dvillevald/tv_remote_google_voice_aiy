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

*Hardware Components:*

![Hardware components](https://github.com/dvillevald/tv_remote_google_voice_aiy/blob/master/images/Hardware_components.jpg)

## Project steps

### Solder wires of 4-pin JST-XH Connector to GPIO pins 24, 26, GND and 5V of Voice HAT (marked by red rectangular below):

![Attaching wires of JST Connector to Voice Hat]





## Software
- LIRC package to detect and send infrared (IR) signals
- Python script 

## Assemble hardware

Follow instructions at (https://aiyprojects.withgoogle.com/voice) and assemble Google Voice AIY kit. 
