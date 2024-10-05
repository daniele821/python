#!/bin/env python3

from scipy.optimize import linprog


def output_solution(linsol, vars=None):
    if not linsol['success']:
        print('ERROR: no solution was found')
    else:
        print("message: " + linsol['message'])
        if vars:
            print("x: ")
        else:
            print("x: " + str(linsol['x']))


def solve_file_v1(file):
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

    linsol = linprog(obj, dis_lhs, dis_rhs, eq_lhs, eq_rhs)
    output_solution(linsol)
    return linsol


# NOTE: in this implementation, vars MUST be string of length one
def parse_linear(vars, invert, linear):
    coeff = [0] * len(vars)
    indexes = []
    for var in vars:
        index = linear.find(var)
        if index != -1:
            indexes.append(index)
    indexes.sort()
    for step, curr in enumerate(indexes):
        prev = 0 if step == 0 else indexes[step-1] + 1
        var = linear[curr]
        var_index = vars.index(var)
        value = linear[prev:curr]
        if value.strip() in ("", "+", "-"):
            value += "1"
        coeff[var_index] = -float(value) if invert else float(value)
    return coeff


def solve_file_v2(file):
    with open(file, "r") as fp:
        lines = fp.read().splitlines()
    lines = [elem for elem in lines if elem.strip()]
    vars = lines[0].split()[1:]
    obj = lines[1].split()
    matrix = lines[2:]
    dis_lhs = []
    dis_rhs = []
    eq_lhs = []
    eq_rhs = []

    # parsing and checking object function
    obj = parse_linear(vars, obj[0] == "max", "".join(obj[1:]))

    # parsing and checking matrix
    for line in matrix:
        index = line.find("=")
        if line[index-1] in "<>":
            index -= 1
        linear = "".join(line[:index].split())
        lhs = parse_linear(vars, line[index] == ">", linear)
        rhs = float(line[index+2:])
        if line[index] == ">":
            rhs *= -1
        if line[index] == "=":
            eq_lhs.append(lhs)
            eq_rhs.append(rhs)
        else:
            dis_lhs.append(lhs)
            dis_rhs.append(rhs)
    if not dis_lhs or not dis_rhs:
        dis_lhs = None
        dis_rhs = None
    if not eq_lhs or not eq_rhs:
        eq_lhs = None
        eq_rhs = None

    linsol = linprog(obj, dis_lhs, dis_rhs, eq_lhs, eq_rhs)
    output_solution(linsol, vars)
    return linsol


solve_file_v1('./input_v1.txt')
solve_file_v2('./input_v2.txt')
