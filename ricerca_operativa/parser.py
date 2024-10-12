#!/bin/env python3

from scipy.optimize import linprog
import numpy as np
import copy


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


def branch_bound():
    with open('branch_bound.txt', 'r') as fp:
        obj, matlhs, matrhs, prop = parse_problem(fp.read())

    tree = []
    nvars = len(obj)

    sol = solve(obj, matlhs, matrhs, prop)
    tree.append(sol)

    index = 0
    while index < len(tree):
        node = tree[index]
        node['integer'] = False
        node['sons'] = []
        node['index'] = index

        if node['success']:
            int_dist = [abs(i - round(i)) for i in node['x']]
            max_dist = max(int_dist)
            max_index = int_dist.index(max(int_dist))
            lhs = node['lhs']
            rhs = node['rhs']
            x = node['x']

            if max_dist > 0:
                tree[index]['sons'] = [len(tree), len(tree) + 1]

                val = x[max_index]
                dis1 = [0] * nvars
                dis1[max_index] = 1
                val1 = int(x[max_index])
                dis2 = [0] * nvars
                dis2[max_index] = -1
                val2 = -(val1 + 1 if val > 0 else -1)
                lhs1 = copy.deepcopy(lhs)
                lhs1.append(dis1)
                lhs2 = copy.deepcopy(lhs)
                lhs2.append(dis2)
                rhs1 = copy.deepcopy(rhs)
                rhs1.append(val1)
                rhs2 = copy.deepcopy(rhs)
                rhs2.append(val2)
                tree.append(solve(obj, lhs1, rhs1, prop))
                tree.append(solve(obj, lhs2, rhs2, prop))

            else:
                node['integer'] = True

        index += 1

    return tree


def print_binary_tree(binary_tree, index=0, level=0, open=set(), lopen=set()):
    solution_node = "\x1b[32;1m"
    invalid_node = "\x1b[31;1m"
    clear = "\x1b[m"
    node = binary_tree[index]
    tmp = ""
    for i in range(level):
        if i == level - 1:
            if i not in lopen:
                tmp += "└── "
            else:
                tmp += "├── "
        else:
            if i in open:
                tmp += "│   "
            else:
                tmp += "    "
    if not node['success']:
        tmp += invalid_node
    elif node['integer']:
        tmp += solution_node
    tmp += str(node['opt'])[:5].ljust(10, ' ')
    tmp += clear
    if node['x']:
        tmp += "["
        tmp += ", ".join([str(i)[:5] for i in node['x']])
        tmp += "]"
    print(tmp)
    open.add(level)
    level += 1
    for i, son in enumerate(node['sons']):
        if i == len(node['sons']) - 2:
            lopen.add(level-1)
        if i == len(node['sons']) - 1:
            open.remove(level - 1)
            lopen.remove(level - 1)
        print_binary_tree(binary_tree, son, level)
    if index == 0:
        print()
    return binary_tree


def solve_binary_tree(binary_tree, output=True):
    buffer = [{
        'opt': i['opt'],
        'x': i['x'],
    } for i in sorted(filter(
        lambda x: x['integer'], binary_tree),
        reverse='max' in binary_tree[0]['prop'],
        key=lambda x: x['opt'])]
    if buffer:
        solution = [i for i in buffer if i['opt'] == buffer[0]['opt']]
        print("optimal value: " + str(solution[0]['opt']))
        print("solutions: ", end="")
        for index, sol in enumerate(solution):
            print(sol['x'], end=" ")
        print()
    else:
        solution = []
        if len(binary_tree) > 1:
            print("no integer solution was found!")
        else:
            print("no solution was found!")
    return solution


solve_binary_tree(print_binary_tree(branch_bound()))
