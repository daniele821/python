#!/bin/python3

with open('names/namesF') as f:
    fname = [x.strip() for x in f.read().splitlines()]

with open('names/namesM') as f:
    mname = [x.strip() for x in f.read().splitlines()]

with open('names/surnames') as f:
    surname = [x.strip() for x in f.read().splitlines()]

    print(fname)
    print(mname)
    print(surname)
