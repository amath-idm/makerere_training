"""
Fit an SIR model to data
"""


# LOAD SOME PACKAGES
import pandas as pd
import numpy as np
import matplotlib.pyplot as pl
from scipy.integrate import odeint
import seaborn as sns

# Read in the data and make a plot
flu = pd.read_csv("influenza_cases.csv")
# pl.plot(flu['day'], flu['cases'])
# pl.xlabel("Day")
# pl.ylabel("Number of cases")
# # pl.show()

# Define our parameters
beta = 3.5
gamma = 1 / 5
npts = 26
I0 = 1
N = 800
dt = 1

# Make arrays where we will store the estimates
x = np.arange(npts)
S = np.zeros(npts)
I = np.zeros(npts)
R = np.zeros(npts)

# Initial conditions
S[0] = N - I0
I[0] = I0

# Simulate the model over time
for t in x[:-1]:
    dS = -beta * S[t] * I[t]/N
    dI = beta * S[t] * I[t]/N - gamma * I[t]
    dR = gamma * I[t]

    S[t + 1] = S[t] + dS * dt
    I[t + 1] = I[t] + dI * dt
    R[t + 1] = R[t] + dR * dt

# Plot the model estimate of the number of infections alongside the data
time = x * dt
pl.plot(time, I, label='Model')
pl.scatter(time, flu['cases'], label='Data')
pl.legend()
pl.show()

