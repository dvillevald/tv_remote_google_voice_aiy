#!/usr/bin/env python3
# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Adds TV remote control functionality to Google Voice AIY kit using the Google Assistant Library.

It is available for Raspberry Pi 2/3 only; Pi Zero is not supported.
"""

"""
My map of LIRC buttons to IR signals (yours will be different):

KEY_POWER                0x42BD807F
KEY_MUTE                 0x42BD40BF
KEY_VOLUMEUP             0x42BD708F
KEY_VOLUMEDOWN           0x42BD30CF
KEY_CHANNELUP            0x42BDD02F
KEY_CHANNELDOWN          0x42BDF00F
KEY_CLOSECD              0x42BDA25D
KEY_HOME                 0x5743C03F 0x5743C13E
KEY_BACK                 0x57436699 0x57436798
KEY_UP                   0x57439867 0x57439966
KEY_DOWN                 0x5743CC33 0x5743CD32
KEY_RIGHT                0x5743B44B 0x5743B54A
KEY_LEFT                 0x57437887 0x57437986
KEY_OK                   0x574354AB 0x574355AA
KEY_PLAY                 0x574332CD 0x574333CC
KEY_FASTFORWARD          0x5743AA55 0x5743AB54
KEY_REWIND               0x57432CD3 0x57432DD2
KEY_SUBTITLE             0x57438679 0x57438778
"""

import logging
import sys
import os
import time
import RPi.GPIO as GPIO
import subprocess

import aiy.assistant.auth_helpers
import aiy.voicehat
from google.assistant.library import Assistant
from google.assistant.library.event import EventType

#time.sleep(10)
#aiy.audio.say('Service activated. I am ready.')

# Name of remote (name) in lircd.conf
remote_name = '/home/pi/lircd.conf'

# Dictionary voice_command_to_key linking voice commands with LIRC remote control button names
voice_command_to_key = {}
voice_command_to_key['turn off TV'] = 'KEY_POWER'
voice_command_to_key['turn on TV'] = 'KEY_POWER'
voice_command_to_key['go home'] = 'KEY_HOME'
voice_command_to_key['select'] = 'KEY_OK'
voice_command_to_key['go up'] = 'KEY_UP'
voice_command_to_key['go down'] = 'KEY_DOWN'
voice_command_to_key['go up'] = 'KEY_UP'
voice_command_to_key['go right'] = 'KEY_RIGHT'
voice_command_to_key['go left'] = 'KEY_LEFT'
voice_command_to_key['go back'] = 'KEY_BACK'
voice_command_to_key['mute'] = 'KEY_MUTE'
voice_command_to_key['stop'] = 'KEY_PLAY'
voice_command_to_key['start'] = 'KEY_PLAY'
voice_command_to_key['volume up'] = 'KEY_VOLUMEUP'
voice_command_to_key['volume down'] = 'KEY_VOLUMEDOWN'
voice_command_to_key['go forward'] = 'KEY_FASTFORWARD'
voice_command_to_key['rewind'] = 'KEY_REWIND'
voice_command_to_key['subtitles'] = 'KEY_SUBTITLE'

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
)

keep_conversation = False

def process_event(event,_assistant):
    global keep_conversation
    status_ui = aiy.voicehat.get_status_ui()
    if event.type == EventType.ON_START_FINISHED:
        status_ui.status('ready')
        if sys.stdout.isatty():
            print('Say "OK, Google" then speak, or press Ctrl+C to quit...')

    elif event.type == EventType.ON_CONVERSATION_TURN_STARTED:
        status_ui.status('listening')

    elif event.type == EventType.ON_END_OF_UTTERANCE:
        status_ui.status('thinking')

    elif event.type == EventType.ON_CONVERSATION_TURN_FINISHED:
        status_ui.status('ready')

    elif event.type == EventType.ON_RECOGNIZING_SPEECH_FINISHED:
        status_ui.status('thinking')
        text = event.args['text']
        if not keep_conversation:
            _assistant.stop_conversation()
        for voice_command in voice_command_to_key.keys():
            if voice_command in text:
                _assistant.stop_conversation()
                if voice_command in ['volume up','volume down']:
                    for pulse in range(6):    
                        lirc_command = "irsend SEND_ONCE " + remote_name + " " + voice_command_to_key[voice_command]
                        print(lirc_command)
                        os.system(lirc_command)
                        time.sleep(0.7)
                else:
                    lirc_command = "irsend SEND_ONCE " + remote_name + " " + voice_command_to_key[voice_command]
                    print(lirc_command)
                    os.system(lirc_command)
                    
        if 'Google shut down' in text:
            _assistant.stop_conversation()
            aiy.audio.say('Shutting down.')
            subprocess.call(["sudo", "shutdown", "-h", "now"])
            
        if 'need your help' in text:
            _assistant.stop_conversation()
            aiy.audio.say('I am listening.')
            keep_conversation = True
        if 'get some rest' in text:
            _assistant.stop_conversation()
            keep_conversation = False
            aiy.audio.say('Let me know when you need my help.')
            
    elif event.type == EventType.ON_RESPONDING_STARTED and event.args and event.args['is_error_response']:
        print(events.args)
        sys.exit(1)
        
    elif event.type == EventType.ON_ASSISTANT_ERROR and event.args and event.args['is_fatal']:
        print(event.args)
        sys.exit(1)

def main():
    credentials = aiy.assistant.auth_helpers.get_assistant_credentials()
    try:
        with Assistant(credentials) as assistant:
            for event in assistant.start():
                process_event(event,assistant)
    finally:            
        GPIO.cleanup()

if __name__ == '__main__':
    main()
