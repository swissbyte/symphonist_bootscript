import RPi.GPIO as GPIO
import time
import requests

LED_SYS = 13  # GPIO13
LED_DAT = 12  # GPIO12
LED_ERR = 30  # GPIO30
KEY_USR = 44
KEY_SYS = 45
LED_ETH = 37
HA_URL = "http://google.ch"


def checkForHALoop():
    while not checkForHA(HA_URL):
        time.sleep(3)


def checkForHA(url):
    try:
        requests.get(url)
    except requests.exceptions.ConnectionError:
        return False
    return True


def sysBlinking():
    GPIO.output(LED_SYS, GPIO.HIGH)
    GPIO.output(LED_DAT, GPIO.LOW)
    GPIO.output(LED_ERR, GPIO.LOW)
    while True:
        GPIO.output(LED_SYS, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(LED_SYS, GPIO.LOW)
        time.sleep(0.5)

def startupAnimation():
    while True:
        GPIO.output(LED_SYS, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(LED_DAT, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(LED_ERR, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(LED_SYS, GPIO.LOW)
        time.sleep(0.5)
        GPIO.output(LED_DAT, GPIO.LOW)
        time.sleep(0.5)
        GPIO.output(LED_ERR, GPIO.LOW)
        time.sleep(0.5)
