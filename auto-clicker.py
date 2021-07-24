import time
import threading
from pynput.mouse import Button, Controller
from pynput.keyboard import Key, Listener, KeyCode

DELAY = 0.001
BUTTON = Button.left
TOGGLE_COMBINATION = {Key.alt_l, KeyCode(char="s")}
EXIT_COMBINATION = {Key.alt_l, KeyCode(char="q")}
CURRENT = set()


class ClickMouse(threading.Thread):
    def __init__(self, delay, button):
        super().__init__()
        self.delay = delay
        self.button = button
        self.running = False
        self.program_running = True

    def start_clicking(self):
        self.running = True

    def stop_clicking(self):
        self.running = False

    def exit(self):
        self.stop_clicking()
        self.program_running = False

    def run(self):
        while self.program_running:
            while self.running:
                mouse.click(self.button)
                time.sleep(self.delay)


mouse = Controller()
click_thread = ClickMouse(DELAY, BUTTON)
click_thread.start()


def on_press(key):
    print("{0} pressed".format(key))
    if key in TOGGLE_COMBINATION:
        CURRENT.add(key)
        if all(keys in CURRENT for keys in TOGGLE_COMBINATION):
            if click_thread.running:
                print("Auto clicker stopped")
                click_thread.stop_clicking()
            else:
                print("Auto clicker started")
                click_thread.start_clicking()
    elif key in EXIT_COMBINATION:
        CURRENT.add(key)
        if all(keys in CURRENT for keys in EXIT_COMBINATION):
            print("Auto clicker exiting...")
            click_thread.exit()
            listener.stop()


def on_release(key):
    try:
        CURRENT.remove(key)
    except KeyError:
        pass


listener = Listener(on_press=on_press, on_release=on_release)
listener.start()
