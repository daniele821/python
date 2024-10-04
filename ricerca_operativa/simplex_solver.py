#!/bin/python3

from scipy.optimize import linprog


def solve_file(file):
    with open(file, "r") as fp:
        lines = fp.read().splitlines()
    lines = [elem for elem in lines if elem.strip()]
    obj = lines[0].split()
    matrix = lines[1:]

    # fixing obj
    if obj[0] == "min":
        obj = [float(elem) for elem in obj[1:]]
    elif obj[0] == "max":
        obj = [-float(elem) for elem in obj[1:]]
    else:
        raise ValueError("invalid input file!")

    # parsing and fixing matrix
    dis_lhs = []
    dis_rhs = []
    eq_lhs = []
    eq_rhs = []
    for line in matrix:
        elems = line.split()
        sign_index = None
        for sign in ("==", "<=", ">="):
            if sign in elems:
                sign_index = elems.index(sign)
        if not sign_index:
            raise ValueError("invalid input file!")
        buffer1 = elems[:sign_index]
        buffer2 = elems[sign_index + 1]
        sign = elems[sign_index]
        match sign:
            case "==":
                eq_lhs.append([float(i) for i in buffer1])
                eq_rhs.append(float(buffer2))
            case ">=":
                dis_lhs.append([-float(i) for i in buffer1])
                dis_rhs.append(-float(buffer2))
            case "<=":
                dis_lhs.append([float(i) for i in buffer1])
                dis_rhs.append(float(buffer2))
    if not dis_lhs or not dis_rhs:
        dis_lhs = None
        dis_rhs = None
    if not eq_lhs or not eq_rhs:
        eq_lhs = None
        eq_rhs = None

    print(linprog(obj, dis_lhs, dis_rhs, eq_lhs, eq_rhs))


solve_file('./input.txt')

# can only solve MINIMIZATION problems
# can only have <= disequations, or == equations
