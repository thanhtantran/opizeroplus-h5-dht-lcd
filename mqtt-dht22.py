import os
import sys
import datetime
import dht11
import time
import paho.mqtt.client as mqtt
import json

from pyA20.gpio import gpio
from pyA20.gpio import port

PIN2 = port.PA6
gpio.init()
#gpio.cleanup()


# read data using pin 2
instance = dht11.DHT11(pin=PIN2)

INTERVAL=2

next_reading = time.time() 

client = mqtt.Client()

client.connect("localhost", 1883, 60)

client.loop_start()

try:
    while True:
        result = instance.read()
        if result.is_valid():
            print("Last valid input: " + str(datetime.datetime.now()))
            print("Temperature: %.2f C" % result.temperature)
            print("Humidity: %.2f %%" % result.humidity)

            client.publish('dht11/temperature', result.temperature, 1)
            client.publish('dht11/humidity', result.humidity, 1)
        time.sleep(2)
except KeyboardInterrupt:
    pass

client.loop_stop()
client.disconnect()
