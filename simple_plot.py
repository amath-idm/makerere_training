'''
Basic plotting example
'''

import numpy as np
import pylab as pl

n = 1000  # Choose how many points to use
x = np.random.randn(n)  # Create x coordinates
y = np.random.randn(n)  # Create y coordinates
c = np.sqrt(x**2 + y**2)  # Set color as distance from center

pl.scatter(x, y, c=c, alpha=0.5)  # Plot
