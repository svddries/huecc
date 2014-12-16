#!/usr/bin/python

import time
import BaseHTTPServer
import json
import phue
import threading

HOST_NAME = ''
PORT_NUMBER = 8000

global BEATMEISTER

# ----------------------------------------------------------------------------------------------------

class BeatMeister:

    def __init__(self):
        self.bridge = phue.Bridge(ip='192.168.178.49', username="2416b7e11a8a0f973722b31520319dab") # Enter bridge IP here.
        self.bridge.connect()

        self.light_name = 'Sfeerlamp Zithoek'
        # light_name = "Hanglamp Eetkamer"

        self.cycle_time = 0

    def run(self):
        t_start = time.time()

        self.stopped = False

        # hue range : 0 - 65535
        beat_hues = [ 0, 10000, 20000, 40000 ]

        while not self.stopped:

            if self.cycle_time == 0:
                time.sleep(0.1)
            else:   
                beat = int((time.time() - t_start) / self.cycle_time) % 4    

                self.bridge.set_light(light_id=self.light_name, parameter={
                    "bri" : 254,
                    "sat" : 254,
                    "hue" : beat_hues[beat] 
                }, transitiontime=0)

                # Sleep until next beat
                t_elapsed = time.time() - t_start
                n = int(t_elapsed / self.cycle_time)
                t_new = (n + 1) * self.cycle_time

                sleep_time = t_new - t_elapsed
                time.sleep(sleep_time)

    def stop(self):
        self.stopped = True

    def set_bpm(self, bpm):
        print "BeatMeister: setting bpm to {0}".format(bpm)
        self.cycle_time = 60.0 / bpm

    def disable(self):
        self.cycle_time = 0

# ----------------------------------------------------------------------------------------------------

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()

    def do_GET(s):
        """Respond to a GET request."""
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        s.wfile.write("<html><head><title>Title goes here.</title></head>")
        s.wfile.write("<body><p>This is a test.</p>")
        # If someone went to "http://something.somewhere.net/foo/bar/",
        # then s.path equals "/foo/bar/".
        s.wfile.write("<p>You accessed path: %s</p>" % s.path)
        s.wfile.write("</body></html>")

    def do_POST(self):
        data_string = self.rfile.read(int(self.headers['Content-Length']))
        self.send_response(200)
        self.end_headers()

        data = json.loads(data_string)

        if data["type"] == "disco":
            BEATMEISTER.set_bpm(data["bpm"])
        else:
            BEATMEISTER.disable()

# ----------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    BEATMEISTER = BeatMeister()

    t = threading.Thread(target=BEATMEISTER.run)
    t.start()

    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    BEATMEISTER.stop()
    t.join()

    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)