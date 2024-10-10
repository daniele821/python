#!/bin/python3

def netmask_to_ip(netmask_abbr):
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

    return netmask


def netmask_to_str(netmask):
    netmask_str = ""
    for i in range(3):
        netmask_str += str(netmask[i])
        netmask_str += "."
    return netmask_str + str(netmask[3])
