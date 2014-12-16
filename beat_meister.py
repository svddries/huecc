#!/usr/bin/python
import phue
import time

bridge = phue.Bridge(ip='192.168.178.49') # Enter bridge IP here.

light_name = 'Sfeerlamp Zithoek'
# light_name = "Hanglamp Eetkamer"

bpm = 124
cycle_time = 60.0 / bpm

beat = 0

# hue range : 0 - 65535
beat_hues = [ 0, 10000, 20000, 40000 ]

t_start = time.time()

while True:
    beat = int((time.time() - t_start) / cycle_time) % 4    

    bridge.set_light(light_id=light_name, parameter={
            "bri" : 254,
            "sat" : 254,
            "hue" : beat_hues[beat] 
        }, transitiontime=0)

    # Sleep until next beat
    t_elapsed = time.time() - t_start
    n = int(t_elapsed / cycle_time)
    t_new = (n + 1) * cycle_time

    sleep_time = t_new - t_elapsed
    time.sleep(sleep_time)


