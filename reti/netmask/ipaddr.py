#!/bin/python3

import sys
from lib import bit_operation, neg, ip_to_str, str_to_ip, binary_ip_to_str, netmask_to_ip
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

    ip = str_to_ip(ipstr)
    netmask = netmask_to_ip(int(netmaskstr))
    host_ip = bit_operation(ip, netmask, lambda x, y: x & y)
    first_ip = bit_operation(host_ip, [0, 0, 0, 1], lambda x, y: x | y)
    broadcast = bit_operation(ip, neg(netmask), lambda x, y: x | y)
    last_ip = bit_operation(broadcast, neg([0, 0, 0, 1]), lambda x, y: x & y)

    ipfmt = ip_to_str(ip)
    netmaskfmt = ip_to_str(netmask)
    hostipfmt = ip_to_str(host_ip)
    firstipfmt = ip_to_str(first_ip)
    lastipfmt = ip_to_str(last_ip)
    broadcastfmt = ip_to_str(broadcast)
    ipfmtb = binary_ip_to_str(ip)
    netmaskfmtb = binary_ip_to_str(netmask)
    hostipfmtb = binary_ip_to_str(host_ip)
    firstipfmtb = binary_ip_to_str(first_ip)
    lastipfmtb = binary_ip_to_str(last_ip)
    broadcastfmtb = binary_ip_to_str(broadcast)

    print("IP and netmask passed are: " + ipfmt.strip() + "/" + netmaskstr)
    print()
    print("------------------------------------------------------------------")
    print("ip address | " + ipfmt + " | " + ipfmtb)
    print("netmask    | " + netmaskfmt + " | " + netmaskfmtb)
    print("-----------+-----------------+------------------------------------")
    print("network id | " + hostipfmt + " | " + hostipfmtb)
    print("broadcast  | " + broadcastfmt + " | " + broadcastfmtb)
    print("-----------+-----------------+------------------------------------")
    print("first id   | " + firstipfmt + " | " + firstipfmtb)
    print("last id    | " + lastipfmt + " | " + lastipfmtb)
    print("------------------------------------------------------------------")
