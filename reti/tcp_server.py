#!/bin/env python3

import lib.ipaddr as ipaddr
import socket as sk

ip = ipaddr.get_ip()
port = 50_000
addr = (ip, port)

socket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
socket.bind(addr)
socket.listen(1)

try:
    while True:
        print('listing on address:', addr)
        stream, raddr = socket.accept()
except KeyboardInterrupt:
    print('closing server')
    socket.close()
