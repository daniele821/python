#!/bin/env python3

import socket as sk
import lib.ipaddr as ipaddr
from time import sleep

rip = '185.141.165.254'
rport = 80
raddr = (rip, rport)

socket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
socket.connect(raddr)
socket.send(
    b'GET /static/hotspot.txt HTTP/1.1\r\nHost: fedoraproject.org\r\n\r\n')
print(socket.recv(2048))
socket.close()
