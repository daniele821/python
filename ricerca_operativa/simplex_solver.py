#!/bin/env python3

import sys
import os
from scipy.optimize import linprog
import numpy as np
import itertools


def warn(msg):
    sys.stderr.write("\x1b[33;1mWARNING: " + msg + "\x1b[0m\n")


def output_solution(linsol, obj, vars):
    if not linsol.success:
        print('ERROR: no solution was found')
        print(linsol.message)
    else:
        print("message: " + linsol.message)
        print("result: " + str(linsol.x))
        for index, var in enumerate(vars):
            print(str(var) + " -> " + str(linsol.x[index]))
        print("optimal: " + str(np.sum(np.array(obj) * np.array(linsol.x))))
        print()


def fmt_coeff(num, var, pos_sign):
    if abs(num) <= np.spacing(1):
        return ""
    value = int(num) if abs(num - int(num)) <= np.spacing(1) else num
    if pos_sign:
        value = str(value) if value <= 0 else "+" + str(value)
    else:
        value = str(value)
    return str(value) + var + " "


def output_matrix(obj, dis_lhs, dis_rhs, eq_lhs, eq_rhs, vars, invert):
    if invert:
        print('max', end=" ")
        obj = [-i for i in obj]
    else:
        print('min', end=" ")
    for i, var in enumerate(vars):
        print(fmt_coeff(obj[i], var, i != 0), end="")
    print()
    if dis_lhs:
        for i, dis in enumerate(dis_lhs):
            nonzero = 0
            for j, var in enumerate(vars):
                print(fmt_coeff(dis[j], var, nonzero != 0), end='')
                if dis[j] != 0:
                    nonzero += 1
            print("<= " + fmt_coeff(dis_rhs[i], "", False))
    if eq_lhs:
        for i, eq in enumerate(eq_lhs):
            nonzero = 0
            for j, var in enumerate(vars):
                print(fmt_coeff(eq[j], var, nonzero != 0), end='')
                if eq[j] != 0:
                    nonzero += 1
            print("== " + fmt_coeff(eq_rhs[i], "", False))
    print()


def convert_to_solver(obj, dis_lhs, dis_rhs, eq_lhs, eq_rhs, vars, unbounded, invert, integer):
    if integer == 1:
        warn("cannot place integer condition to online solver\n")
    with open(os.path.dirname(__file__) + '/solver.txt', "w") as fp:
        for var in vars:
            fp.write("var " + var)
            if not unbounded:
                fp.write(" >= 0")
            fp.write(";\n")
        fp.write("\n")
        if invert:
            fp.write("maximize optimal :")
            obj = [-i for i in obj]
        else:
            fp.write("minimize optimal :")
        for i, var in enumerate(vars):
            if obj[i] != 0:
                val = str(obj[i]) if obj[i] < 0 else "+" + str(obj[i])
                fp.write(" " + val + "*" + var)
        fp.write(";\n\n")
        cond = 1
        if dis_lhs:
            for i, dis in enumerate(dis_lhs):
                fp.write("subject to c" + str(cond) + ":")
                cond += 1
                for j, var in enumerate(vars):
                    if dis[j] != 0:
                        val = str(dis[j]) if dis[j] < 0 else "+" + str(dis[j])
                        fp.write(" " + val + "*" + var)
                fp.write(" <= ")
                val = str(
                    dis_rhs[i]) if dis_rhs[i] < 0 else "+" + str(dis_rhs[i])
                fp.write(val)
                fp.write(";\n")
        if eq_lhs:
            for i, eq in enumerate(eq_lhs):
                fp.write("subject to c" + str(cond) + ":")
                cond += 1
                for j, var in enumerate(vars):
                    if eq[j] != 0:
                        val = str(eq[j]) if eq[j] < 0 else "+" + str(eq[j])
                        fp.write(" " + val + "*" + var)
                fp.write(" == ")
                val = str(
                    eq_rhs[i]) if eq_rhs[i] < 0 else "+" + str(eq_rhs[i])
                fp.write(val)
                fp.write(";\n")
        fp.write("\nend;\n")


def output_all_vertexes(obj, dis_lhs, dis_rhs, eq_lhs, eq_rhs, vars):
    dis_lhs = dis_lhs or [[]]
    dis_rhs = dis_rhs or []
    eq_lhs = eq_lhs or [[]]
    eq_rhs = eq_rhs or []
    lhs = dis_lhs + eq_lhs
    rhs = dis_rhs + eq_rhs
    dimension = len(dis_rhs) + len(eq_rhs)
    for x in itertools.combinations(range(dimension), len(obj)):
        A = [lhs[i] for i in x]
        b = [rhs[i] for i in x]
        sol = np.linalg.solve(A, b)
        opt = np.sum(np.array(obj) * sol)
        correct = True
        if dis_rhs:
            for index, dis in enumerate(dis_lhs):
                if np.sum(np.array(dis) * sol) > dis_rhs[index]:
                    correct = False
        if eq_rhs:
            for index, eq in enumerate(eq_lhs):
                if abs(np.sum(np.array(eq) * sol) - eq_rhs[index]) > np.spacing(1):
                    correct = False
        if correct:
            print(str(sol).ljust(23, ' '), ' --> ', opt)


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
        coeff[var_index] += -float(value) if invert else float(value)
    return coeff


# NOTE: in this implementation, vars can be of any lenght
def parse_linear_v2(vars, invert, linear):
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
        coeff[var_index] += -float(value) if invert else float(value)
    return coeff


def solve_file(file):
    with open(file, "r") as fp:
        lines = fp.read().splitlines()
    lines = [e for e in lines if e.strip() and not e.startswith("//")]
    vars = lines[0].split()[1:]
    obj = lines[1].split()
    unbounded = "unbound" in lines[0].split()[0]
    integer = "int" in lines[0].split()[0]
    invert = obj[0] == "max"
    matrix = lines[2:]
    dis_lhs = []
    dis_rhs = []
    eq_lhs = []
    eq_rhs = []

    # parsing stuff
    bounds = (0, None) if not unbounded else (None, None)
    integer = 1 if integer else 0

    # parsing and checking object function
    obj = parse_linear_v2(vars, invert, "".join(obj[1:]))

    # parsing and checking matrix
    for line in matrix:
        index = line.find("=")
        if line[index-1] in "<>":
            index -= 1
        linear = "".join(line[:index].split())
        lhs = parse_linear_v2(vars, line[index] == ">", linear)
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
                     eq_rhs, bounds, integrality=integer)
    output_matrix(obj, dis_lhs, dis_rhs, eq_lhs, eq_rhs, vars, invert)
    output_solution(linsol, [-i for i in obj] if invert else obj, vars)
    convert_to_solver(obj, dis_lhs, dis_rhs, eq_lhs,
                      eq_rhs, vars, unbounded, invert, integer)
    return linsol


solve_file(os.path.dirname(__file__) + '/input.txt')
