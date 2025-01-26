#!/bin/env python3

from scipy.optimize import linprog
import numpy as np
import copy
import os

SCRIPT_PATH = os.path.realpath(__file__)
SCRIPT_DIR = os.path.dirname(SCRIPT_PATH)


# parsers
def parse_linear_v1(vars, linear):
    '''
    doesn't support
        - variable names of lenght > 1
        - ripetition of the same variable
        - space between -/+ and numeric value
    '''
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
            coeff[var_index] += float(value)
        return coeff


def parse_linear_v2(vars, linear):
    '''
    supports:
        - variable names of lenght > 1
    doesn't support
        - ripetition of the same variable
        - space between -/+ and numeric value
    '''
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


def parse_linear_v3(vars, linear):
    '''
    supports:
        - variable names of lenght > 1
        - ripetition of the same variable
    doesn't support:
        - space between -/+ and numeric value
    '''
    coeff = [0] * len(vars)
    indexes = []
    indlen = {0: 0}
    nums = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "-", "+", " "]
    for i in range(len(linear)):
        if linear[i] not in nums:
            for var in vars:
                if linear[i:].startswith(var):
                    indexes.append(i)
                    indlen[i] = len(var)
    for step, curr in enumerate(indexes):
        prev = 0 if step == 0 else indexes[step-1]
        var = linear[curr:curr+indlen[curr]]
        var_index = vars.index(var)
        value = linear[prev+(indlen[prev]):curr]
        if value.strip() in ("", "+", "-"):
            value += "1"
        coeff[var_index] += float(value)
    return coeff


def parse_linear_v4(vars, linear):
    '''
    supports:
        - variable names of lenght > 1
        - ripetition of the same variable
        - space between -/+ and numeric value
    '''
    coeff = [0] * len(vars)
    indexes = []
    indlen = {0: 0}
    nums = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "-", "+", " "]
    for i in range(len(linear)):
        if linear[i] not in nums:
            for var in vars:
                if linear[i:].startswith(var):
                    indexes.append(i)
                    indlen[i] = len(var)
    for step, curr in enumerate(indexes):
        prev = 0 if step == 0 else indexes[step-1]
        var = linear[curr:curr+indlen[curr]]
        var_index = vars.index(var)
        value = "".join(linear[prev+(indlen[prev]):curr].split())
        if value.strip() in ("", "+", "-"):
            value += "1"
        coeff[var_index] += float(value)
    return coeff


def parse_linear(vars, linear):
    return parse_linear_v4(vars, linear)


def parse_problem(file):
    filepath = os.path.join(file)
    with open(filepath, 'r') as fp:
        input = fp.read()
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
                prop.add(line.split()[0])
            else:
                status += 1
        if status == 3:
            sign_index = line.rfind("=")
            buffer_lhs = parse_linear(vars, line[:sign_index-1])
            buffer_rhs = float("".join(line[sign_index+1:].split()))
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
    bound = (None, None)
    integer = 0
    propPos = "positive" in prop
    propInt = "integer" in prop
    propBin = "binary" in prop
    if propPos:
        bound = (0, None)
    if propInt:
        integer = 1
    if propBin:
        integer = 1
        bound = (0, 1)
    res = linprog(obj, mat_lhs, mat_rhs, bounds=bound, integrality=integer)
    solution = {'success': res.success, 'message': res.message}
    if res.success:
        x = [int(i) if i == int(i) else float(i) for i in res.x]
        if propInt:
            x = [round(i) for i in x]
        opt = np.sum(np.array(obj) * np.array(res.x))
        opt = float(-opt if "max" in prop else opt)
        if propInt:
            opt = round(opt)
        solution['x'] = x
        solution['opt'] = copy.deepcopy(opt)
    else:
        solution['x'] = None
        solution['opt'] = None
    solution['lhs'] = copy.deepcopy(mat_lhs)
    solution['rhs'] = copy.deepcopy(mat_rhs)
    solution['obj'] = copy.deepcopy(obj)
    solution['prop'] = copy.deepcopy(prop)
    return solution


def solve_file(file):
    obj, mat_lhs, mat_rhs, prop = parse_problem(file)
    return solve(obj, mat_lhs, mat_rhs, prop)


solution = solve_file("programmazione_lineare.txt")
if (solution['success']):
    print("\x1b[1;32m" + solution['message'] + "\x1b[m")
    print("\x1b[1;37m" + "SOLUTION:      \x1b[1;34m" + str(solution['x']) + "\x1b[m")
    opt = solution['opt']
    print("\x1b[1;37m" + "OPTIMAL VALUE: \x1b[1;34m" + str(opt) + "\x1b[m")
else:
    print("\x1b[1;31m" + solution['message'] + "\x1b[m")
