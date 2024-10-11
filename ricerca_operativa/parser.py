#!/bin/env python3

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


def parse_problem(input):
    lines = input.splitlines()
    lines = [e.strip() for e in lines if e.strip() and not e.startswith("//")]

    prop = set()
    vars = []
    obj = []
    mat_lhs = []
    mat_rhs = []

    status = 0
    for line in lines:
        if status == 0:
            if line.startswith("vars"):
                status += 1
            else:
                prop.add(line)
        if status == 1:
            if not vars:
                vars = line.split()[1:]
            else:
                status += 1
        if status == 2:
            if not obj:
                obj = parse_linear(vars, "".join(line.split()[1:]))
                if line.split()[0] == "max":
                    obj = [-i for i in obj]
            else:
                status += 1
        if status == 3:
            sign_index = line.rfind("=")
            buffer_lhs = parse_linear(vars, line[:sign_index-1])
            buffer_rhs = float(line[sign_index+1:])
            negbuf_lhs = [-i for i in buffer_lhs]
            negbuf_rhs = -buffer_rhs
            if line[sign_index-1] != ">":
                mat_lhs.append(buffer_lhs)
                mat_rhs.append(buffer_rhs)
            if line[sign_index-1] != "<":
                mat_lhs.append(negbuf_lhs)
                mat_rhs.append(negbuf_rhs)

    return obj, mat_lhs, mat_rhs, prop


def solve(obj, mat_lhs, mat_rhs, prop):
    bound = (None, None) if "unbounded" in prop else (0, None)
    integer = 1 if "integer" in prop else 0
    return linprog(obj, mat_lhs, mat_rhs, bounds=bound, integrality=integer)


def solve_file(file):
    with open(file, "r") as fp:
        obj, mat_lhs, mat_rhs, prop = parse_problem(fp.read())
        return solve(obj, mat_lhs, mat_rhs, prop)


print(solve_file('input.txt'))
