#!/usr/bin/python

import time
import BaseHTTPServer
import json
import phue

# Plugins
from plugins.beat_meister import BeatMeister

HOST_NAME = ''
PORT_NUMBER = 8000

PLUGINS = {}
CURRENT_PLUGIN = None

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

        try:
            plugin_name = data["type"]

            if plugin_name in PLUGINS.keys():
                global CURRENT_PLUGIN
                if CURRENT_PLUGIN:
                    CURRENT_PLUGIN.stop()

                CURRENT_PLUGIN = PLUGINS[plugin_name]
                CURRENT_PLUGIN.set_data(data)
                CURRENT_PLUGIN.start()
            else:
                print "Unknown plugin: " + plugin_name
        except KeyError:
            print "JSON request does not contain field 'type'."

# ----------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # Connect to Philips Hue bridge
    bridge = phue.Bridge(ip='192.168.178.49', username="2416b7e11a8a0f973722b31520319dab")
    bridge.connect()

    # Set plugins
    PLUGINS = { "beat_meister" : BeatMeister(bridge) }
    CURRENT_PLUGIN = None

    # Create HTTP server
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    
    # Run HTTP server
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    if CURRENT_PLUGIN:
        CURRENT_PLUGIN.stop()

    # Close HTTP server
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)