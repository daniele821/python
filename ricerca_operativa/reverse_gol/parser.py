#!/bin/env python3

import os
import copy
import numpy as np
from scipy.optimize import linprog
from pathlib import Path

SCRIPT_PATH = os.path.realpath(__file__)
SCRIPT_DIR = os.path.dirname(SCRIPT_PATH)
INITPOS_FILE = SCRIPT_DIR + "/init_pos.in"
INPUT_FILE = SCRIPT_DIR + "/gol.txt"


# parsers
def parse_linear_v1(vars, linear):
    '''
    doesn't support
        - variable names of lenght > 1
        - ripetition of the same variable
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


def parse_linear(vars, linear):
    return parse_linear_v3(vars, linear)


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
    bound = bound if "binary" not in prop else (0, 1)
    integer = integer if "binary" not in prop else 1
    res = linprog(obj, mat_lhs, mat_rhs, bounds=bound, integrality=integer)
    solution = {'success': res.success, 'message': res.message}
    if res.success:
        x = [int(i) if i == int(i) else float(i) for i in res.x]
        opt = np.sum(np.array(obj) * np.array(res.x))
        opt = float(-opt if "max" in prop else opt)
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


# init input file
def oneD_to_twoD(index, size):
    return index / size, index % size


def twoD_to_oneD(a, b, size):
    return a * size + b


def init_input_file():
    initpos = Path(INITPOS_FILE).read_text()
    output = open(INPUT_FILE, "w")

    lines = initpos.splitlines()
    size = len(lines)
    totalsize = size * size
    output.write("binary\n\nvars ")
    for i in range(totalsize):
        output.write("x" + str(i) + " ")
    output.write("\n\nmin\n\n")
    golarr = ([0] * size) * size
    for a, line in enumerate(lines):
        for b, char in enumerate(line):
            if char == "@":
                golarr[twoD_to_oneD(a, b, size)] = 1

    print(golarr)

    output.close()


init_input_file()
