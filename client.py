import socket
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
            keyboard.tap(Key.up) #youtube volume up
            keyboard.press(Key.ctrl_l) #spotify volume up
            keyboard.tap(Key.up)
            keyboard.release(Key.ctrl_l)
        case "Thumbs Down":
            keyboard.tap(Key.down) #youtube volume down 
            keyboard.press(Key.ctrl_l) #spotify volume down
            keyboard.tap(Key.down)
            keyboard.release(Key.ctrl_l)
        case "Point Up":
            for i in range (volume_amt):
                keyboard.tap(Key.media_volume_up)
        case "Point Down":
            for i in range (volume_amt):
                keyboard.tap(Key.media_volume_down)
        case "Point Left":
            keyboard.tap(Key.media_previous)
        case "Point Right":
            keyboard.tap(Key.media_next)
        case "Lol":
            keyboard.press(Key.alt)
            keyboard.press(Key.f4)
            keyboard.release(Key.alt)
            keyboard.release(Key.f4)


def main(): 
    while True:
        IP = "192.168.0.121"
        PORT = 6900
        keyboard = Controller()
        HEADERSIZE = 8

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((IP, PORT))
        except:
            print("No connection available yet! Trying again in 5 seconds...")
            time.sleep(5)
            continue


        while True:
            connection_lost = False
            full_msg = ''
            new_msg = True
            while True:
                msg = s.recv(128)
                if new_msg:
                    if msg == b'':
                        s.close()
                        connection_lost = True
                        break
                    msglen = int(msg[:HEADERSIZE])
                    new_msg = False
                full_msg += msg.decode("utf-8")

                if len(full_msg)-HEADERSIZE == msglen:
                    gesture = full_msg[HEADERSIZE:]
                    if (gesture != "none"):
                        print(gesture)
                        executeCommand(gesture, keyboard)
                    new_msg = True
                    full_msg = ""
            if connection_lost:
                break

if __name__ == "__main__":
    main()