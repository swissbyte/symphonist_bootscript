import os
import subprocess
import RPi.GPIO as GPIO
import time
import requests

LED_SYS = 13  # GPIO13
LED_DAT = 12  # GPIO12
LED_ERR = 30  # GPIO30
KEY_USR = 44
KEY_SYS = 45
LED_ETH = 37
WIFISHDN = 42
HA_URL = "http://google.ch"

animationRun = True


def initGPIO():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_SYS, GPIO.OUT)
    GPIO.setup(LED_DAT, GPIO.OUT)
    GPIO.setup(LED_ERR, GPIO.OUT)
    GPIO.setup(LED_ETH, GPIO.OUT)
    GPIO.setup(KEY_SYS, GPIO.IN)
    GPIO.setup(KEY_USR, GPIO.IN)
    # GPIO.setup(WIFISHDN, GPIO.OUT)


def checkForHALoop():
    while not checkForHA(HA_URL):
        time.sleep(3)


def resetWiFi():
    # reset WiFi
    GPIO.output(WIFISHDN, GPIO.LOW)
    time.sleep(0.2)
    GPIO.output(WIFISHDN, GPIO.HIGH)


def checkForHA(url):
    try:
        requests.get(url)
    except requests.exceptions.ConnectionError:
        return False
    return True


def sysShuttingDown():
    GPIO.output(LED_SYS, GPIO.LOW)
    GPIO.output(LED_DAT, GPIO.LOW)
    GPIO.output(LED_ERR, GPIO.LOW)
    time.sleep(0.5)
    GPIO.output(LED_SYS, GPIO.HIGH)
    GPIO.output(LED_DAT, GPIO.HIGH)
    GPIO.output(LED_ERR, GPIO.HIGH)
    time.sleep(0.5)


def sysBlinking():
    GPIO.output(LED_SYS, GPIO.HIGH)
    GPIO.output(LED_DAT, GPIO.LOW)
    GPIO.output(LED_ERR, GPIO.LOW)
    while True:
        GPIO.output(LED_SYS, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(LED_SYS, GPIO.LOW)
        time.sleep(0.5)


def resetBlinking():
    while True:
        GPIO.output(LED_SYS, GPIO.LOW)
        GPIO.output(LED_DAT, GPIO.LOW)
        GPIO.output(LED_ERR, GPIO.LOW)
        time.sleep(0.2)
        GPIO.output(LED_SYS, GPIO.HIGH)
        GPIO.output(LED_DAT, GPIO.HIGH)
        GPIO.output(LED_ERR, GPIO.HIGH)
        time.sleep(0.2)


def startupAnimation():
    while animationRun:
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

def setAllLEDon():
    GPIO.output(LED_SYS, GPIO.HIGH)
    GPIO.output(LED_DAT, GPIO.HIGH)
    GPIO.output(LED_ERR, GPIO.HIGH)

def waitForWifi():
    while "wlan0" not in os.listdir('/sys/class/net/'):
        GPIO.output(LED_SYS, GPIO.HIGH)
        time.sleep(0.2)
        GPIO.output(LED_SYS, GPIO.LOW)
        time.sleep(0.2)


def cmdSUDO(command):
    sudoPassword = ''
    # command = 'mount -t vboxsf myfolder /home/myuser/myfolder'
    p = os.system('echo %s|sudo -S %s' % (sudoPassword, command))


def resetToAPMode():
    if not os.path.isfile('/etc/raspiwifi/host_mode'):
      cmdSUDO("python3 /usr/lib/raspiwifi/reset_device/manual_reset.py")
      resetBlinking()

def startWiFiConfig():
    if os.path.isfile('/etc/raspiwifi/host_mode'):
        # subprocess.call("/usr/lib/raspiwifi/reset_device/static_files/aphost_bootstrapper")
        cmdSUDO("sh /usr/lib/raspiwifi/reset_device/static_files/aphost_bootstrapper")
    else:
        # subprocess.call("/usr/lib/raspiwifi/reset_device/static_files/apclient_bootstrapper")
        cmdSUDO("sh /usr/lib/raspiwifi/reset_device/static_files/apclient_bootstrapper")
