#!/bin/env python3

import numexpr


def _output_(expr_str, res, accumulator, output):
    if output:
        print(expr_str, '=', res)
    else:
        accumulator.append([expr_str, str(res)])


def _solve_eq_(expr_str, solution, output, accumulator):
    try:
        res = numexpr.evaluate(expr_str)
    except Exception:
        res = None
    if solution is None:
        _output_(expr_str, res, accumulator, output)
        return
    if type(solution) is tuple:
        match len(solution):
            case 1:
                if res == solution[0]:
                    _output_(expr_str, res, accumulator, output)
            case 2:
                if res is None:
                    return
                if res >= solution[0] and res <= solution[1]:
                    _output_(expr_str, res, accumulator, output)
            case _:
                if res in solution:
                    _output_(expr_str, res, accumulator, output)
        return
    if solution == res:
        _output_(expr_str, res, accumulator, output)
        return


def find_operators(operators=['+', '-', '*', '/'], nums=[8, 1, 1, 5], iterate_orders=True, solution=None, output=True):
    """
        - operators: specify all valid operators to fill in the gaps
        - nums: numbers making up the left side of the equation
        - iterate_orders : enable iterating all possible positions of a pair of brackets
        - solution: - None -> show all equations (even those with no result)
                    - value -> show only equations which result is exactly that value
                    - tuple: - of size 1 -> show only equations which result is exactly that value
                             - of size 2 -> show only equations which result in between those values
                             - of size 3 -> show only equations which result is one of those values
        - output: if True print to stdout, otherwise return a list of all results
    """

    optypes = len(operators)
    ops = len(nums)
    gaps = ops - 1
    iter = [0] * ops
    accumulator = None if output else []

    if ops < 1:
        return

    for num in range(optypes**gaps):
        # initialize iter list
        for i in range(ops):
            iter[i] = (num // ops**i) % optypes

        # build up the nth expression as a string
        if iterate_orders and solution is None and output:
            print('----------------------------')
        expr = [str(nums[0])]
        for i in range(1, ops):
            expr.append(operators[iter[i-1]])
            expr.append(str(nums[i]))
        _solve_eq_(''.join(expr), solution, output, accumulator)

        # for each nth expression, build all possible () positioning
        if iterate_orders:
            for a in range(ops):
                for b in range(a, ops):
                    expr2 = expr[:b*2+1]+[')']+expr[b*2+1:]
                    expr2 = expr2[:a*2]+['(']+expr2[a*2:]
                    _solve_eq_(''.join(expr2), solution, output, accumulator)

    return accumulator
