#!/bin/env python3

import numexpr


def _solve_eq_(expr_str):
    try:
        return numexpr.evaluate(expr_str)
    except Exception:
        return None


def find_operators(operators=['+', '-', '*', '/'], nums=[8, 1, 1, 5], iterate_orders=True, solution=None):
    """
        - operators: specify all valid operators to fill in the gaps
        - nums: numbers making up the left side of the equation
        - iterate_orders : enable iterating all possible positions of a pair of brackets
        - solution: if not None, show only expression with result equal to it
    """

    optypes = len(operators)
    ops = len(nums)
    gaps = ops - 1
    iter = [0] * ops

    if ops < 1:
        return

    for num in range(optypes**gaps):
        # initialize iter list
        for i in range(ops):
            iter[i] = (num // ops**i) % optypes

        # build up the nth expression as a string
        if iterate_orders and solution is None:
            print('----------------------------')
        expr = [str(nums[0])]
        for i in range(1, ops):
            expr.append(operators[iter[i-1]])
            expr.append(str(nums[i]))
        expr_str = ''.join(expr)
        res = _solve_eq_(expr_str)
        if solution is None or solution == res:
            print(expr_str, '=', res)

        # for each nth expression, build all possible () positioning
        if iterate_orders:
            for a in range(ops):
                for b in range(a, ops):
                    expr2 = expr[:b*2+1]+[')']+expr[b*2+1:]
                    expr2 = expr2[:a*2]+['(']+expr2[a*2:]
                    expr2_str = ''.join(expr2)
                    res = _solve_eq_(expr2_str)
                    if solution is None or solution == res:
                        print(expr2_str, '=', res)
