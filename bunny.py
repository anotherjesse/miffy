from machine import Pin, Timer
from neopixel import NeoPixel
import time

numPixels = 23
pin = 13
np = NeoPixel(Pin(pin, Pin.OUT), numPixels)

color = (0, 0, 0)
glow_color = (0, 0, 0)
grow = False
tick = 0

timer = None


def stop_glow():
    global timer
    if timer:
        timer.deinit()
        timer = None


def glow(new_color):
    global timer
    global glow_color

    glow_color = new_color
    if not timer:
        timer = Timer(-1)
        timer.init(period=5000, mode=Timer.PERIODIC, callback=glow_cb)


def glow_cb():
    global color
    global glow_color
    if glow_color == color:
        setColor((0, 0, 0))
    else:
        setColor(glow_color)


def setColor(newColor):
    global color
    color = newColor


def draw():
    global tick

    tick += 1

    if grow:
        p = tick % numPixels
        if np[p] == color:
            np[p] = (0, 0, 0)
        else:
            np[p] = color
    else:
        for p in range(0, numPixels):
            np[p] = color
    np.write()


# def growShrinkRing(color):
#     for p in range(0, numPixels):
#         np[p] = [0, 0, 0]
#     np.write()
#     for p in range(0, numPixels):
#         np[p] = color
#         np.write()
#         time.sleep_ms(50)
#     for p in range(0, numPixels):
#         np[p] = [0, 0, 0]
#         np.write()
#         time.sleep_ms(50)
