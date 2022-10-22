import threading
import time
import pyautogui
import win32api
import win32con
from pynput.keyboard import Listener, KeyCode
from pynput.mouse import Controller

tile_R_color_range = range(1, 20)

s_key = KeyCode(char='s')  # start and stop key
e_key = KeyCode(char='e')  # exit key


def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def proximity(target_1: [list[int]], target_2: list[int], prox: int):
    return abs(target_1[0] - target_2[0] <= prox) or abs(
        target_1[1] - target_2[1] <= prox)


def positions(prox: int, region, color):  # get the targets positions to click
    pic = pyautogui.screenshot(region=region)
    width, height = pic.size
    targets = []
    for x in range(0, width, prox):
        for y in range(0, height, prox):
            if pic.getpixel((x, y)) == color:
                target_already_registered_index = -1
                for i in range(0, len(targets)):
                    target = targets[i]
                    if proximity(target[len(target) - 1], [x, y], prox):  # if proximity is less than prox parameter
                        target_already_registered_index = i  # target already registered in position i
                        break
                if target_already_registered_index >= 0:
                    targets[target_already_registered_index].append([x, y])
                else:
                    targets.append([[x, y]])

    # in targets, we have all the pixels that forms each target, we need only one pixel to click

    pixels_to_click = []

    for i in range(0, len(targets)):
        pixels_target = targets[i]
        middle = int((len(pixels_target) / 2))
        pixels_to_click.append(pixels_target[middle])

    return pixels_to_click


class Bot(threading.Thread):
    def __init__(self):
        super(Bot, self).__init__()
        self.running = False
        self.program_running = True
        print("ready")

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
                pos = positions(5, (95, 460, 750, 500), (255, 219, 195))
                for i in pos:
                    click(i[0] + 95, i[1] + 460)
                time.sleep(0.05)
            time.sleep(0.00001)  # delay for catching the keyboard I/O for stopping and starting the program


# creates everything
mouse = Controller()  # the mouse
click_thread = Bot()  # thread
click_thread.start()  # starts the thread


# for stopping and starting

def key_press(key):  # key press
    if key == s_key:
        if click_thread.running:
            click_thread.stop_clicking()  # stop
            print("stopped")
        else:
            click_thread.start_clicking()  # start
            print("startedss")
    elif key == e_key:  # exit
        click_thread.exit()
        listener.stop()


with Listener(on_press=key_press) as listener:  # listener
    listener.join()
