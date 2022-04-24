from pynput.keyboard import Key, Controller

def main():
    keyboard = Controller()
    keyboard.press(Key.alt)
    keyboard.press(Key.f4)
    keyboard.release(Key.alt)
    keyboard.release(Key.f4)


if __name__ == "__main__":
    main()