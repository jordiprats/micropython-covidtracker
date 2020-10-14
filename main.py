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
    tm.write([0b00111100, 0b10011110, 0b11111000, 0b11110001])

def error_bug():
    global tm
    tm.write([0b01111100, 0b00111110, 0b10111101, 0b01101111])
    utime.sleep(5)
    tm.write([0b01111100, 0b00111110, 0b10111101, 0b01111111])
    utime.sleep(5)
    tm.write([0b01111100, 0b00111110, 0b10111101, 0b00000111])
    utime.sleep(5)
    tm.write([0b01111100, 0b00111110, 0b10111101, 0b01111101])
    utime.sleep(5)
    tm.write([0b01111100, 0b00111110, 0b10111101, 0b01101101])
    utime.sleep(5)
    tm.write([0b01111100, 0b00111110, 0b10111101, 0b01100110])
    utime.sleep(5)
    tm.write([0b01111100, 0b00111110, 0b10111101, 0b01001111])
    utime.sleep(5)
    tm.write([0b01111100, 0b00111110, 0b10111101, 0b01011011])
    utime.sleep(5)
    tm.write([0b01111100, 0b00111110, 0b10111101, 0b00000110])
    utime.sleep(5)
    tm.write([0b01111100, 0b00111110, 0b10111101, 0b00111111])
    utime.sleep(5)

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

while True:

    try:
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

        while True:
            covidcache_url = covid_config['baseurl']+'/school/'+covid_config['school']
            print(covidcache_url)

            r = urequests.get(covidcache_url)
            data = json.loads(r.text)

            if "WTF" in data.keys():
                error_wtf()
                utime.sleep(30)
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

                # grups confinats
                tm.number(data['groups_confinats'])
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
        error_bug()



