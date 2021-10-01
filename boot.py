import bunny
import time
import uos
import machine
from network import WLAN
import gc
import ubinascii
import webrepl
from umqttsimple import MQTTClient

wlan = WLAN()
# wlan.config(dhcp_hostname='miffy')

webrepl.start()
gc.collect()

def waitForWlan():
    color = 0
    dx = 1
    while not wlan.isconnected():
        color += dx
        if color == 255:
            dx = -1
        elif color == 0:
            dx = 1
        bunny.setColor((color, color, color))
        bunny.draw()
        time.sleep_ms(10)

waitForWlan()
bunny.setColor((0, 255, 0))
bunny.draw()
