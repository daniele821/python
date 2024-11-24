#!/bin/python3

import os

SCRIPT_PATH = os.path.realpath(__file__)
SCRIPT_DIR = os.path.dirname(SCRIPT_PATH)
OUTPUT = SCRIPT_DIR + "/gol.txt"

print(OUTPUT)
