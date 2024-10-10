#!/bin/python3

import sys
import lib

input = sys.argv[1:]
ipaddr = [0, 0, 0, 0]
netmask = [0, 0, 0, 0]

if len(input) == 0:
    exit(0)

ip_uses_dots = False
try:
    int(input[0])
except Exception:
    ip_uses_dots = True


if ip_uses_dots:
    input_nospace = ''.join(''.join(input).split())
