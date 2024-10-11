#!/bin/python3


def netmask_to_ip(netmask_abbr):
    if netmask_abbr < 0 or netmask_abbr > 32:
        raise ValueError('invalid abbreviated netmask')
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


def ip_to_str(ip):
    netmask_str = ""
    for i in range(3):
        netmask_str += str(ip[i])
        netmask_str += "."
    netmask_str += str(ip[3])
    return netmask_str.ljust(15, ' ')


def binary_ip_to_str(ip):
    def int_to_binary(value):
        acc = ''
        for i in reversed(range(8)):
            mask = 1 << i
            acc += str((value & mask) // mask)
        return acc
    netmask_str = ""
    for i in range(3):
        netmask_str += int_to_binary(ip[i])
        netmask_str += "."
    netmask_str += int_to_binary(ip[3])
    return netmask_str


def str_to_ip(ipstr):
    ip_vals = ipstr.split('.')
    if len(ip_vals) != 4:
        raise ValueError('invalid ip address string')
    ip = []
    for ip_val in ip_vals:
        ip_val = int(ip_val)
        if ip_val < 0 or ip_val > 255:
            raise ValueError('invalid ip address string')
        ip.append(ip_val)
    return ip


def bit_operation(ip1, ip2, operation):
    res = []
    for i in range(4):
        res.append(operation(ip1[i], ip2[i]))
    return res


def neg(ip):
    return bit_operation(ip, ip, lambda x, _: ~x & 0xff)
