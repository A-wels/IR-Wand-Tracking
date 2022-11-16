import requests
import RPi.GPIO as gpio
import time

def toggle_hexalight() -> None:
    url = "http://192.168.178.101:8123/api/webhook/wled-wz"
    x = requests.post(url)
    print("Hexalight toggle")



def trigger_motor():
    gpio.setmode(gpio.BCM)
    gpio.setup(5,gpio.OUT)
    gpio.setup(6,gpio.OUT)
    print("one")
    gpio.output(5,False)
    gpio.output(6,True)
    time.sleep(4.5)
    print("two")
    gpio.output(6, False)
    time.sleep(3)
    gpio.output(5,True)
    gpio.output(6,False)
    time.sleep(4)
    print("stop")
    gpio.output(5,False)
    gpio.output(6,False)
    time.sleep(2)
    gpio.cleanup()
