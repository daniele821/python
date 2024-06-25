#!/bin/python3

import random

LINES = 2000

with open('names/namesF') as f:
    fname = [x.strip() for x in f.read().splitlines()]

with open('names/namesM') as f:
    mname = [x.strip() for x in f.read().splitlines()]

with open('names/surnames') as f:
    surname = [x.strip() for x in f.read().splitlines()]

res = set()
while len(res) < LINES/2:
    res.add((random.choice(fname), random.choice(surname), 'F'))
while len(res) < LINES:
    res.add((random.choice(mname), random.choice(surname), 'M'))

for name, surname, sex in res:
    print(name, surname, sex)
