#!/bin/python3

import sys
import lib

# input: values between 0,32 representing a netmask
# output: netmask in dot notation

if __name__ == "__main__":
    for i in range(1, len(sys.argv[1:]) + 1):
        netmask_abbr = int(sys.argv[i])
        netmask = lib.netmask_to_ip(netmask_abbr)

        print(str(netmask_abbr).ljust(2, " "), end=" | ")
        print(lib.ip_to_str(netmask) + " | " + lib.binary_ip_to_str(netmask))
