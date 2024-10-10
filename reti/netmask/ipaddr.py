#!/bin/python3

import sys
import lib
import subprocess
# input: ip [/netmask]
# output: ip, netmask, net id, host id range

if __name__ == "__main__":
    input = ''.join(''.join(sys.argv[1:]).split())
    if not input:
        input = subprocess.getoutput(
            "nmcli dev show wlp1s0 | grep -i 'ip4.address'").split()[1]
    sep_index = input.find('/')
    ipstr = input[:sep_index] if sep_index != -1 else input
    netmaskstr = input[sep_index+1:] if sep_index != -1 else ''
    netmaskstr = netmaskstr if netmaskstr else '32'

    ip = lib.str_to_ip(ipstr)
    netmask = lib.netmask_to_ip(int(netmaskstr))
    host_ip = lib.bit_operation(ip, netmask, lambda x, y: x & y)
    broadcast = lib.bit_operation(ip, netmask, lambda x, y: x | (~y & 0xff))

    print("IP and netmask passed are: " +
          lib.ip_to_str(ip).strip() + "/" + netmaskstr)
    print()
    print("ip address | " + lib.ip_to_str(ip) +
          " | " + lib.binary_ip_to_str(ip))
    print("netmask    | " + lib.ip_to_str(netmask) +
          " | " + lib.binary_ip_to_str(netmask))
    print("network id | " + lib.ip_to_str(host_ip) +
          " | " + lib.binary_ip_to_str(host_ip))
    print()
    print("network id | " + lib.ip_to_str(host_ip) +
          " | " + lib.binary_ip_to_str(host_ip))
    print("broadcast  | " + lib.ip_to_str(broadcast) +
          " | " + lib.binary_ip_to_str(broadcast))
