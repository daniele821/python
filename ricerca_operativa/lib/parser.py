#!/bin/python3

from scipy.optimize import linprog


def parse_linear(vars, linear):
    coeff = [0] * len(vars)
    indexes = []
    indlen = {0: 0}
    for var in vars:
        index = linear.find(var)
        if index != -1:
            indexes.append(index)
            indlen[index] = len(var)
    indexes.sort()
    for step, curr in enumerate(indexes):
        prev = 0 if step == 0 else indexes[step-1]
        var = linear[curr:curr+indlen[curr]]
        var_index = vars.index(var)
        value = linear[prev+(indlen[prev]):curr]
        if value.strip() in ("", "+", "-"):
            value += "1"
        coeff[var_index] += float(value)
    return coeff


def solve_file(input):
    lines = input.splitlines()
    lines = [e for e in lines if e.strip() and not e.startswith("/")]
    vars = lines[0].split()[1:]
    obj = lines[1].split()[1:]
    matrix = lines[2:]

    dis_lhs = []
    dis_rhs = []
    eq_lhs = []
    eq_rhs = []

    is_unbounded = "unbound" in lines[0].split()[0]
    is_continuos = "int" not in lines[0].split()[0]
    is_min = lines[1].split() == "min"
    prop = []

    # parsing stuff
    prop.append((0, None) if not is_unbounded else (None, None))
    prop.append(0 if is_continuos else 1)

    # parsing and checking object function
    obj = parse_linear(vars, "".join(obj[1:]))

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
    linsol = linprog(obj, dis_lhs, dis_rhs, eq_lhs,
                     eq_rhs, prop[0], integrality=prop[1])

    return linsol
