#!/bin/env python3

import socket as sk


def create_dns_message(domain_name: str) -> bytes:
    print('todo')


def send_dns_message(dns_message: bytes):
    resolver_ip = '127.0.0.53'
    resolver_port = 53
    resolver_addr = (resolver_ip, resolver_port)
    socket = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
    socket.sendto(dns_message, resolver_addr)
    socket.close()


send_dns_message(bytes('hi there!'.encode()))
