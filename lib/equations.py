#!/bin/env python3

import numexpr


def find_operators(operators=['+', '-', '*', '/'], nums=[8, 1, 1, 5]):
    """
        - operators must be a list of strings of a single char
        - nums must be a list of numbers of a single digit
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
        print('----------------------------')
        expr = str(nums[0])
        for i in range(1, ops):
            expr += operators[iter[i-1]]
            expr += str(nums[i])

        # for each nth expression, build all possible () positioning
        for a in range(ops):
            for b in range(a, ops):
                expr2 = expr[:b*2+1]+')'+expr[b*2+1:]
                expr2 = expr2[:a*2]+'('+expr2[a*2:]
                try:
                    res = numexpr.evaluate(expr2)
                except Exception:
                    res = None
                print(expr2, '=', res)
