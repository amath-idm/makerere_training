"""
Fit an SIR model to data
"""


# Load packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as pl

# Read in the data and make a plot
flu = pd.read_csv("influenza_cases.csv")
# pl.plot(flu['day'], flu['cases'])
# pl.xlabel("Day")
# pl.ylabel("Number of cases")
# # pl.show()

# Define our parameters
beta = 0.5
gamma = 0.2
npts = 100
I0 = 1
N = 1000
dt = 1

# Make arrays where we will store the estimates
x = np.arange(npts)
S = np.zeros(npts)
I = np.zeros(npts)
R = np.zeros(npts)

# Initial conditionsbeta * S[t] * I[t]/N
S[0] = N - I0
I[0] = I0

# Simulate the model over time
for t in x[:-1]:
    infections = beta * S[t] * I[t]/N * dt
    recoveries = gamma * I[t] * dt

    S[t + 1] = S[t] - infections
    I[t + 1] = I[t] + infections - recoveries
    R[t + 1] = R[t] + recoveries

# Plot the model estimate of the number of infections alongside the data
time = x * dt
pl.plot(time, I, label='Model')
# pl.scatter(time, flu['cases'], label='Data')
pl.legend()
pl.show()

