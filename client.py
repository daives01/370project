import socket
import sys
import time
from pynput.keyboard import Key, Controller

def executeCommand(msg, keyboard):
    volume_amt = 5
    match msg:
        case "Open Hand":
            keyboard.tap(Key.media_play_pause)
        case "Fist":
            keyboard.tap(Key.media_volume_mute)
        case "Thumbs Up":
            for i in range (volume_amt):
                keyboard.tap(Key.media_volume_up)
        case "Thumbs Down":
            for i in range (volume_amt):
                keyboard.tap(Key.media_volume_down)
        case "Point Up":
            keyboard.tap(Key.up)
        case "Point Down":
            keyboard.tap(Key.down)
        case "Point Left":
            keyboard.tap(Key.media_previous)
        case "Point Right":
            keyboard.tap(Key.media_next)
        case "Lol":
            keyboard.type("Hey!")



keyboard = Controller()
HEADERSIZE = 8

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.50.170", 4202))

while True:
    full_msg = ''
    new_msg = True
    while True:
        msg = s.recv(128)
        print(msg)
        if new_msg:
            msglen = int(msg[:HEADERSIZE])
            new_msg = False
        full_msg += msg.decode("utf-8")

        if len(full_msg)-HEADERSIZE == msglen:
            gesture = full_msg[HEADERSIZE:]
            print(gesture)
            if (gesture != "None Detected"):
                executeCommand(gesture, keyboard)
            new_msg = True
            full_msg = ""
