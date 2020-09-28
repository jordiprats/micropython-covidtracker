import gc
import re
import utime


debug = True

from config import wifi_config
from config import covid_config

import tm1637
from machine import Pin
tm = tm1637.TM1637(clk=Pin(5), dio=Pin(4))
tm.brightness(1)
tm.write([0, 0, 0, 0])
tm.write([127, 255, 127, 127])

if debug: print('leds init')

import network

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
    import urequests

    gc.collect()
    #r = urequests.get('https://tracacovid.akamaized.net/data.csv')
    r = urequests.get('https://tracacovid.akamaized.net/data.csv')

    for line in r.iter_lines():
        if line:
            if re.search(';'+str(covid_config['school'])+';', line):
                if debug: print(line)
except Exception as e:
    if debug: print('unhandled exception')
    if debug: print(str(e))