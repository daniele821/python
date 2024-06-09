#!/bin/env python3

from lib.threexplusone import *
from lib.equations import *

import numpy as np

res = find_operators(output=False, solution=3)
res = [x[1] for x in res]
print(res)
