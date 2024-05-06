#!/bin/env python3

import socket as sk
import random


def create_dns_message(domain_name: str) -> bytes:
    identifier = bytes([random.randint(0, 255), random.randint(0, 255)])
    flags = bytes([0x01, 0x20])
    QDcount = bytes([0x00, 0x01])
    ANcount = bytes([0x00, 0x00])
    NScount = bytes([0x00, 0x00])
    ARcount = bytes([0x00, 0x01])
    flags = bytes([0x01, 0x20])
    return identifier + flags + QDcount + ANcount + NScount + ARcount


def send_dns_message(dns_message: bytes):
    resolver_ip = '127.0.0.53'
    resolver_port = 53
    resolver_addr = (resolver_ip, resolver_port)
    socket = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
    socket.sendto(dns_message, resolver_addr)
    socket.close()


send_dns_message(create_dns_message('google.com'))
