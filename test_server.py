#!/usr/bin/python
import httplib
import json

import time

conn = httplib.HTTPConnection("localhost", 8000)

# -------------------------------------------------------------

#conn.request("GET", "/")
#r = conn.getresponse()
#print r.status, r.reason
#print r.read()

# -------------------------------------------------------------

num_beats = 16

raw_input("Beat 1...")
t_start = time.time()

for i in range(2, num_beats+1):
    raw_input("Beat {0}".format(i))

bpm = 60 / ((time.time() - t_start) / (num_beats - 1))

print "Beats per minute: {0}".format(bpm)

data = { "type" : "beat_meister", "bpm" : bpm}

conn.request("POST", "/", json.dumps(data))
r = conn.getresponse()


conn.close()