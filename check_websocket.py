#!/usr/bin/python

import socket
import ssl
import argparse
import re
import sys
from urlparse import urlparse

parser = argparse.ArgumentParser(description="WebSocket test")
parser.add_argument('-u', help="Websocket URL", required=True)
parser.add_argument('-s', help="Secure WebSocket", action="store_true")

if not vars(parser.parse_args())['s']:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
else:
    s = ssl.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), ssl_version=ssl.PROTOCOL_SSLv23)

url = urlparse(vars(parser.parse_args())['u'])
if url.port is None:
    if url.scheme is 'https':
        port = 443
    else:
        port = 80
else:
    port = int(url.port)

try:
    s.connect((url.hostname,port))
    s.send('GET ' + url.path + ' HTTP/1.1\r\n')
    s.send('Connection: upgrade\r\n')
    s.send('Upgrade: websocket\r\n')
    s.send('Host: ' + url.hostname + '\r\n')
    s.send('Origin: ' + url.scheme + '://' + url.hostname + '\r\n')
    s.send('Sec-WebSocket-Key: 2G418csYFXXRKjwlDDYMcwo=\r\n')
    s.send('Sec-WebSocket-Version: 13\r\n\r\n')
    data = s.recv(1024)
    s.close()
except:
    e = sys.exc_info()[0]
    print("Problem with WebSocket Connection: " + str(e))
    exit(2)

data = data.replace('\r\n',' ')
if re.search('^HTTP\/1\.1\ 101', data):
    print("WebSocket Connection Successful:" + repr(data))
    exit(0)
else:
    print("Problem with WebSocket Connection: " + repr(data))
    exit(2)
