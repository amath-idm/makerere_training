"""
Fit an SIR model to data
"""


# Load packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as pl

# Read in the data and make a plot
flu = pd.read_csv("flu_cases.csv")

# Define our parameters
beta1 = .5
gamma1 = 1/50
beta2 = .6
gamma2 = 1/10
npts = 100
I0 = 1
N = 1000
dt = 1

# Make arrays where we will store the estimates
x = np.arange(npts) 
S1 = np.zeros(npts)
I1 = np.zeros(npts)
R1 = np.zeros(npts)
S2 = np.zeros(npts)
I2 = np.zeros(npts)
R2 = np.zeros(npts)

# Initial conditions
S1[0] = N - I0
I1[0] = I0
S2[0] = N - I0
I2[0] = I0

# Simulate the model over time
for t in x[:-1]:

    infections1 = beta1 * S1[t] * I1[t]/N * dt
    recoveries1 = gamma1 * I1[t] * dt
    infections2 = beta2 * S2[t] * I2[t]/N * dt
    recoveries2 = gamma2 * I2[t] * dt

    S1[t + 1] = S1[t] - infections1
    I1[t + 1] = I1[t] + infections1 - recoveries1
    R1[t + 1] = R1[t] + recoveries1

    S2[t + 1] = S2[t] - infections2
    I2[t + 1] = I2[t] + infections2 - recoveries2
    R2[t + 1] = R2[t] + recoveries2

# # Plot the model estimate of the number of infections alongside the data
time = x * dt
# pl.plot(time, I, label='Model')
# pl.scatter(time, flu['cases'], label='Data')
# pl.legend()
# pl.show()

# Plot just the first few days
pl.plot(time[:25], I1[:25], label=f'beta={beta1}, gamma={gamma1}, R0={beta1/gamma1:.2f}')
pl.plot(time[:25], I2[:25], label=f'beta={beta2}, gamma={gamma2}, R0={beta2/gamma2:.2f}')
pl.scatter(time[:25], flu['cases'][:25], label='Data')
pl.legend()
pl.show()

