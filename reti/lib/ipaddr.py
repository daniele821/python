#!/bin/env python3

import socket


def get_ip():
    return socket.gethostbyname(socket.gethostname())


if __name__ == "__main__":
    print(get_ip())
