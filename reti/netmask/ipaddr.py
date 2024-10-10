#!/bin/python3

import sys
import lib

# input: ip [/netmask]
# output: ip, netmask, net id, host id range

if __name__ == "__main__":
    input = ''.join(''.join(sys.argv[1:]).split())
    sep_index = input.find('/')
    ipstr = input[:sep_index] if sep_index != -1 else input
    netmaskstr = input[sep_index+1:] if sep_index != -1 else ''
    netmaskstr = netmaskstr if netmaskstr else '32'

    ip = lib.str_to_ip(ipstr)
    netmask = lib.netmask_to_ip(int(netmaskstr))
    host_id = lib.host_ip(ip, netmask)

    print("ip address | " + lib.ip_to_str(ip) +
          " | " + lib.binary_ip_to_str(ip))
    print("netmask    | " + lib.ip_to_str(netmask) +
          " | " + lib.binary_ip_to_str(netmask))
    print("host id    | " + lib.ip_to_str(host_id) +
          " | " + lib.binary_ip_to_str(host_id))
