#!/bin/env python3

import socket as sk
import lib.ipaddr as ipaddr
from time import sleep

rip = ipaddr.get_ip()
rport = 50000
raddr = (rip, rport)

socket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
print('created socket:', socket)
socket.connect(raddr)
print('established connection with:', raddr)
sleep(10)
socket.close()
print('connection closed!')
