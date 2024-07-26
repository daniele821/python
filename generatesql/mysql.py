#!/bin/python3

import fileinput
from codicefiscale import codicefiscale
from random import randint as rand


def cf(a, b, c, d, e):
    return codicefiscale.encode(a, b, c, d, e)


RUOLO = 'hostess'
check1 = set()
check2 = set()
for line in fileinput.input():
    words = line.split()
    name = words[0]
    surname = words[1]
    gender = words[2]
    year = str(rand(1940, 2000))
    month = str(rand(1, 12))
    day = str(rand(1, 28))
    date = year + '-' + month + '-' + day
    dateRev = day + '/' + month + '/' + year
    dateAssunzione = str(rand(2000, 2020)) + '-' + \
        str(rand(1, 12)) + '-' + str(rand(1, 28))
    birthplace = 'Cesena'
    CF = cf(surname, name, gender, dateRev, birthplace)
    if CF in check1:
        raise Exception('there is a duplicate codice fiscale')
    check1.add(CF)
    print('( \''+name+'\', \'' + surname+'\', \'' + CF + '\', \'' +
          date+'\', \'' + dateAssunzione + '\', \'' + RUOLO + '\'),')
