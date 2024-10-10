#!/bin/python3

import sys
import lib

if __name__ == "__main__":
    for i in range(1, len(sys.argv[1:]) + 1):
        netmask_abbr = int(sys.argv[i])
        netmask = lib.netmask_to_ip(netmask_abbr)

        print(str(netmask_abbr).ljust(5, " "), end="")

        print(lib.netmask_to_str(netmask))
