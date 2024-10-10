#!/bin/python3

import sys
import lib

# input: ip [/netmask]
# output: ip, netmask, net id, host id

input = sys.argv[1:]
ipaddr = [0, 0, 0, 0]
netmask = [0, 0, 0, 0]

input_nospace = ''.join(''.join(input).split())
