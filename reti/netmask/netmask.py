#!/bin/python3

import sys

for i in range(1, len(sys.argv[1:]) + 1):
    netmask_abbr = int(sys.argv[i])
    if netmask_abbr < 0 or netmask_abbr > 32:
        raise ValueError('invalid netmask')
    netmask = [0, 0, 0, 0]

    full_bytes = netmask_abbr // 8
    last_byte = netmask_abbr % 8
    for i in range(full_bytes):
        netmask[i] = 255

    match last_byte:
        case 0: pass
        case 1: netmask[full_bytes] = 0b1000_0000
        case 2: netmask[full_bytes] = 0b1100_0000
        case 3: netmask[full_bytes] = 0b1110_0000
        case 4: netmask[full_bytes] = 0b1111_0000
        case 5: netmask[full_bytes] = 0b1111_1000
        case 6: netmask[full_bytes] = 0b1111_1100
        case 7: netmask[full_bytes] = 0b1111_1110

    print(str(netmask_abbr).ljust(5, " "), end="")

    print(str(netmask[0]) + '.' + str(netmask[1]) +
          '.' + str(netmask[2]) + '.' + str(netmask[3]))
