#!/bin/python3

import sys
import random

try:
    LENGTH = int(sys.argv[1])
except:
    LENGTH = 20

with open('passeggeri') as f:
    listCF = [x.strip() for x in f.read().splitlines()]

res = set()
while len(res) < LENGTH:
    res.add(random.choice(listCF))

for elem in res:
    print(elem)
