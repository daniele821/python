#!/bin/env python3

from lib.threexplusone import *
from lib.equations import *

import numpy as np

res = find_operators(output=False, skipNone=True, solution=(1, 10, 10))
res = np.array([x[1] for x in res], dtype=np.float128)
print(np.unique(np.sort(res)))
