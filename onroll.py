import RPi.GPIO as gpio
import time
def trigger_motor():
    gpio.setmode(gpio.BCM)
    gpio.setup(5,gpio.OUT)
    gpio.setup(6,gpio.OUT)
    print("one")
    print("two")
    gpio.output(5,False)
    gpio.output(6,True)
    time.sleep(3)
    print("stop")
    gpio.output(5,False)
    gpio.output(6,False)
    gpio.cleanup()

trigger_motor()
