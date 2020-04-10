import os

if "wlan0" in os.listdir('/sys/class/net/'):
    print("WLAN0 exists!")
