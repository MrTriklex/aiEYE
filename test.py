from threading import Thread
from time import sleep, perf_counter
import keyboard_emu as kbe


def func(idx, status: callable = None):
    while True:
        position = status()
        print(position)
        if position < 300:
            if position > 0:
                kbe.key_press(kbe.SC_RIGHT)

            if position < 0:
                kbe.key_press(kbe.SC_LEFT)
        else:
            break


global_status = 211


def my_status():
    global global_status
    return global_status


th = Thread(target=func, args=(0, my_status))
th.start()
while True:
    for st in range(1):
        sleep(0.1)
        global_status += 10
        if global_status > 300:
            global_status = 211
        print(12345)