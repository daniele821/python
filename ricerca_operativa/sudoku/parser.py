#!/bin/env python3

from scipy.optimize import linprog
import numpy as np
import copy
import os


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


# sudoku solver
def build_sudoku_matrix(sol_arr):
    sudoku = [[0 for x in range(9)] for y in range(9)]
    for value in range(9):
        for a in range(9):
            for b in range(9):
                index = value * 81 + a * 9 + b
                sudoku_value = sol_arr[index]
                if sudoku_value:
                    sudoku[a][b] = value + 1
    return sudoku


def print_sudoku_matrix(sudoku):
    print("┌───────┬───────┬───────┐")
    for i in range(9):
        for j in range(9):
            if j % 3 == 0:
                print("│", end=" ")
            val = sudoku[i][j]
            val = val if val else " "
            print(val, end=" ")
        print("│")
        if i % 3 == 2 and i != 8:
            print("├───────┼───────┼───────┤")
    print("└───────┴───────┴───────┘")


def print_sudoku_grid():
    print("┌──────────┬──────────┬──────────┐")
    for i in range(9):
        for j in range(9):
            if j % 3 == 0:
                print("│", end=" ")
            val = str(i + 1) + str(j + 1)
            print(val, end=" ")
        print("│")
        if i % 3 == 2 and i != 8:
            print("├──────────┼──────────┼──────────┤")
    print("└──────────┴──────────┴──────────┘")


def view_sudoku():
    obj, matlhs, matrhs, prop = parse_problem(
        os.path.dirname(os.path.realpath(__file__)) + '/sudoku.txt')
    sol = solve(obj, matlhs, matrhs, prop)
    x = sol['x']
    print_sudoku_matrix(build_sudoku_matrix(x))
    if os.getenv("DBG") is not None:
        print(x)
        for a in range(9):
            index = a * 81
            buffer = [x[index+i*9:index+(i+1)*9] for i in range(9)]
            for i in range(9):
                for j in range(9):
                    buffer[i][j] *= a + 1
            print_sudoku_matrix(buffer)


# actual execution
view_sudoku()
