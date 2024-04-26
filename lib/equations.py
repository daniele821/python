#!/bin/env python3

def find_operators(operators=['+', '-', '*', '/'], nums=[8, 1, 1, 5]):
    import numexpr
    ops = len(operators)
    for i in operators:
        for j in operators:
            for k in operators:
                expr = str(nums[0]) + i + str(nums[1])
                expr += j + str(nums[2]) + k + str(nums[3])
                for a in range(ops):
                    for b in range(a, ops):
                        expr2 = expr[:b*2+1]+')'+expr[b*2+1:]
                        expr2 = expr2[:a*2]+'('+expr2[a*2:]
                        try:
                            print(expr2, '=', numexpr.evaluate(expr2))
                        except Exception:
                            print(expr2, '=', 'Nil')
