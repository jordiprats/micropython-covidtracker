from config import wifi_config
from config import covid_confi
from machine import Pin
import gc
import re
import utime
import network
import tm1637

def school_open():
    global tm
    tm.write([0b00111111, 0b01111100, 0b01010100, 0b01111000])

def school_closed():
    global tm
    tm.hex(0xdead)


debug = True

tm = tm1637.TM1637(clk=Pin(5), dio=Pin(4))
tm.brightness(1)
tm.write([0, 0, 0, 0])
tm.write([127, 255, 127, 127])

if debug: print('leds init')

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.scan()
sta_if.connect(wifi_config['ssid'], wifi_config['password'])

if not sta_if.isconnected():
    sta_if.connect()
    print("Waiting for connection...")
    while not sta_if.isconnected():
        utime.sleep(1)
print(sta_if.ifconfig())

try:
    # covidcache

except Exception as e:
    if debug: print('unhandled exception')
    if debug: print(str(e))