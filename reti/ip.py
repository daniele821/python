#!/bin/env python3

import socket as sk
from time import time

counter = 0
start = time()
initial = start

with sk.socket(sk.AF_INET, sk.SOCK_RAW, sk.IPPROTO_TCP) as ipsocket:
    while True:
        ipsocket.recv(5_000)
        counter += 1
        if time() - start > 1:
            start = time()
            print(str(counter) + ' tcp packets received! ['
                  + str(time() - initial) + ']')
