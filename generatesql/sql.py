#!/bin/python3

import fileinput
from codicefiscale import codicefiscale
from random import randint as rand
import random
import string


def randomword(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def cf(a, b, c, d, e):
    return codicefiscale.encode(a, b, c, d, e)


check1 = set()
check2 = set()
for line in fileinput.input():
    words = line.split()
    name = words[0]
    surname = words[1]
    gender = words[2]
    date = str(rand(1, 28)) + '/' + str(rand(1, 12)) + \
        '/' + str(rand(1920, 2020))
    birthplace = 'Cesena'
    email = name + '.' + surname + '@' + \
        ['gmail.com', 'outlook.com'][rand(0, 1)]
    password = randomword(8)
    CF = cf(surname, name, gender, date, birthplace)
    if CF in check1:
        raise Exception('there is a duplicate codice fiscale')
    if email in check2:
        raise Exception('there is a duplicate email')
    check1.add(CF)
    check2.add(email)
    print('( \''+name+'\', \'' + surname+'\', \'' + CF + '\', \'' + email+'\', \'' + password + '\'),')
