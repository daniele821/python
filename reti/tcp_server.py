#!/bin/env python3

import lib.ipaddr as ipaddr
import socket as sk

ip = ipaddr.get_ip()
port = 51_000
addr = (ip, port)

socket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
socket.bind(addr)
socket.listen(1)
print('listing on address:', addr)

try:
    while True:
        stream, raddr = socket.accept()
        print('established connection with:', raddr)
except KeyboardInterrupt:
    print('closing server')
    socket.close()
