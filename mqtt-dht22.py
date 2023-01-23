import os
import sys
import datetime
import dht22
import time
import paho.mqtt.client as mqtt
import json

from pyA20.gpio import gpio
from pyA20.gpio import port

PIN2 = port.PA6
gpio.init()
#gpio.cleanup()


# read data using pin 14
instance = dht22.DHT22(pin=PIN2)

sensor_data = {'temperature': 0, 'humidity': 0, 'time': null}

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
            sensor_data['temperature'] = result.temperature
            sensor_data['humidity'] = result.humidity
            sensor_data['time'] = str(datetime.datetime.now())
            client.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)

        time.sleep(2)
except KeyboardInterrupt:
    pass

client.loop_stop()
client.disconnect()