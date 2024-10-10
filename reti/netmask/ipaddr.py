#!/bin/python3

import sys
from netmask import netmask_to_str, netmask_to_ip

input = sys.argv[1:]
args = len(input)

match args:
    # xxx.xxx.xxx.xxx[/xx]
    case 1: print(1)
    # xxx.xxx.xxx.xxx[ /xx|/ xx| / xx | xx]
    case 2 | 3: print(2)
