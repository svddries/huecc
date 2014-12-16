#!/usr/bin/python
from phue import Bridge
import random

b = Bridge(ip='192.168.178.49') # Enter bridge IP here.

#If running for the first time, press button on bridge and run with b.connect() uncommented
#b.connect()

lights = b.get_light_objects()

h = 0
b = 254
while True:
    for light in lights:
        if light.name == "Sfeerlamp Zithoek":
            light.brightness = b
            light.saturation = 254            
            light.hue = h % 65535
        if light.name == "Plafondlamp Zithoek":
            light.brightness = b
            light.saturation = 254            
            light.hue = (h + 20000) % 65535
        if light.name == "Hanglamp Eetkamer":
            light.brightness = b
            light.saturation = 254            
            light.hue = (h + 40000) % 65535
    h += 10000
    #b = 254 - b


