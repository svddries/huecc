#!/usr/bin/python
import httplib
import json

conn = httplib.HTTPConnection("localhost", 8000)

# -------------------------------------------------------------

#conn.request("GET", "/")
#r = conn.getresponse()
#print r.status, r.reason
#print r.read()

# -------------------------------------------------------------

data = { "type" : "disco", "bpm" : 124}

conn.request("POST", "/", json.dumps(data))
r = conn.getresponse()


conn.close()