#!/bin/env python3

import numexpr


def find_operators(operators=['+', '-', '*', '/'], nums=[8, 1, 1, 5], iterate_orders=True):
    """
        - operators: specify all valid operators to fill in the gaps
        - nums: numbers making up the left side of the equation
        - iterate_orders : enable iterating all possible positions of a pair of brackets
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
        if iterate_orders:
            print('----------------------------')
        expr = [str(nums[0])]
        for i in range(1, ops):
            expr.append(operators[iter[i-1]])
            expr.append(str(nums[i]))
        expr_str = ''.join(expr)
        try:
            res = numexpr.evaluate(expr_str)
        except Exception:
            res = None
        print(expr_str, '=', res)

        # for each nth expression, build all possible () positioning
        if iterate_orders:
            for a in range(ops):
                for b in range(a, ops):
                    expr2 = expr[:b*2+1]+[')']+expr[b*2+1:]
                    expr2 = expr2[:a*2]+['(']+expr2[a*2:]
                    expr2_str = ''.join(expr2)
                    try:
                        res = numexpr.evaluate(expr2_str)
                    except Exception:
                        res = None
                    print(expr2_str, '=', res)
