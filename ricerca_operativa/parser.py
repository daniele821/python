#!/bin/env python3


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


def parse_file(input):
    lines = input.splitlines()
    lines = [e.strip() for e in lines if e.strip() and not e.startswith("//")]

    properties = set()
    vars = []
    obj = []
    matrixes_lhs = [[], [], []]
    matrixes_rhs = [[], [], []]

    status = 0
    for line in lines:
        if status == 0:
            if line.startswith("vars"):
                status += 1
            else:
                properties.add(line)
        if status == 1:
            if not vars:
                vars = line.split()[1:]
            else:
                status += 1
        if status == 2:
            if not obj:
                obj = parse_linear(vars, "".join(line.split()[1:]))
            else:
                status += 1
        if status == 3:
            sign_index = line.rfind("=")
            match line[sign_index-1]:
                case "<": pos = 0
                case ">": pos = 1
                case "=": pos = 2
            matrixes_lhs[pos].append(parse_linear(vars, line[:sign_index-1]))
            matrixes_rhs[pos].append(float(line[sign_index+1:]))

    return (properties, vars, obj, matrixes_lhs, matrixes_rhs)
