from config import wifi_config
from config import covid_config
from machine import Pin
import urequests
import network
import tm1637
import utime
import json
import re
import gc

def loading():
    global tm
    tm.write([0b10000000, 0b10000000, 0b10000000, 0b10000000])

def error_wtf():
    global tm
    tm.write([0b00000000, 0b00101010, 0b01111000, 0b01110001])

def school_open():
    global tm
    tm.write([0b00111111, 0b01111100, 0b01010000, 0b01111000])

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
loading()
utime.sleep(5)

try:
    while True:
        covidcache_url = covid_config['baseurl']+'/school/'+covid_config['school']
        print(covidcache_url)

        r = urequests.get(covidcache_url)
        data = json.loads(r.text)

        if "WTF" in data.keys():
            error_wtf()
            utime.sleep(120)
            continue

        # 1 hora i poc - per tindre la cache expirada
        for i in range(0, 200):
            # ultim update
            tm.number(data['ultim_update'])
            utime.sleep(5)

            # estat cole
            if data['estat_centre']=='Obert':
                school_open()
            else:
                school_closed()
            utime.sleep(5)

            # confinats
            tm.number(data['confinats'])
            utime.sleep(5)

            # positius
            tm.number(data['positius'])
            utime.sleep(5)



except Exception as e:
    if debug: print('unhandled exception')
    if debug: print(str(e))
    error_wtf()
    utime.sleep(120)
    machine.reset()