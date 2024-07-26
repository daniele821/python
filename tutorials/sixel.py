#!/bin/env python3

import matplotlib.pyplot as plt
# this directly runs matplotlib with sixel as its backend
import matplotlib
matplotlib.use('module://matplotlib-backend-sixel')
# set this in the shell from where you are running the python code
# MPLBACKEND='module://matplotlib-backend-sixel'

plt.plot([1, 2, 3], [3, 4, 5])
plt.show()

plt.plot([1, 2, 3], [3, 4, 5])
plt.show()
