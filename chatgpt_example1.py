import numpy as np
import matplotlib.pyplot as plt

np.random.seed(1)

n = 1000
x1 = np.random.normal(size=n)
y1 = x1 + np.random.normal(size=n)

plt.scatter(x1, y1)
plt.plot(np.unique(x1), np.poly1d(np.polyfit(x1, y1, 1))(np.unique(x1)), color='red')
plt.show()
