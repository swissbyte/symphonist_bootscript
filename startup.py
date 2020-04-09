import ctypes

import RPi.GPIO as GPIO
import time
import requests

import SymSys as sys
from threading import Thread

# Dies ist ein Kommentar
print("Zeile1")  # noch ein Kommentar
# print("Zeile2")
print("Zeile 3")

GPIO.setmode(GPIO.BCM)
GPIO.setup(sys.LED_SYS, GPIO.OUT)
GPIO.setup(sys.LED_DAT, GPIO.OUT)
GPIO.setup(sys.LED_ERR, GPIO.OUT)
GPIO.setup(sys.LED_ETH, GPIO.OUT)
GPIO.setup(sys.KEY_SYS, GPIO.IN)
GPIO.setup(sys.KEY_USR, GPIO.IN)


def buttonPress(*args):
    print("ButtonPressed")


GPIO.add_event_detect(sys.KEY_USR, edge=GPIO.FALLING, callback=buttonPress, bouncetime=200)

animation = Thread(target=sys.startupAnimation)
animation.start()


try:
    requests.get("http://gosogle.com")
except requests.exceptions.ConnectionError:
    animation.do_run = False;
    animation.join()
    animation = Thread(target=sys.sysBlinking)
    # AP has been started automatically and this will restart the system anyway.
    animation.join()

animation.do_run = False;
animation.join()

print("End animation")

print(sys.checkForHA("http://googlfe.ch"))

print("Total end")
