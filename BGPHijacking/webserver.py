#!/bin/bash

# Copyright 2021
# Georgia Tech
# All rights reserved
# Do not post or publish in any public or forbidden forums or websites
import http.server
import socketserver
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--text', default="Default web server")
FLAGS = parser.parse_args()

class Handler(http.server.SimpleHTTPRequestHandler):
    # Disable logging DNS lookups
    def address_string(self):
        return str(self.client_address[0])

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write("<h1>{}</h1>\n".format(FLAGS.text).encode('UTF-8'))
        self.wfile.flush()


PORT = 80
httpd = socketserver.TCPServer(("", PORT), Handler)
httpd.serve_forever()
