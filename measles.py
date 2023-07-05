"""
Model for measles
"""


# Load packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as pl 

# Define our parameters without treatment
R0 = 17
gamma_no_treatment = 1/25
beta = R0*gamma_no_treatment

# Define our parameters with treatment
gamma_with_treatment = 1/10

# Initial conditions and other settings
npts = 100
I0 = 1
N = 1000
dt = 1

# Make arrays where we will store the estimates
x = np.arange(npts)
S = np.zeros(npts)
I = np.zeros(npts)
R = np.zeros(npts)
# Copy the arrays to store the results with treatment
ST = np.zeros(npts)
IT = np.zeros(npts)
RT = np.zeros(npts)

# Initial conditions
S[0] = N - I0
I[0] = I0
ST[0] = N - I0
IT[0] = I0

# Simulate the model over time
for t in x[:-1]:

    infections = beta * S[t] * I[t]/N * dt
    recoveries = gamma_no_treatment * I[t] * dt

    infectionsT = beta * ST[t] * IT[t]/N * dt
    recoveriesT = gamma_with_treatment * IT[t] * dt

    S[t + 1] = S[t] - infections
    I[t + 1] = I[t] + infections - recoveries
    R[t + 1] = R[t] + recoveries

    ST[t + 1] = ST[t] - infectionsT
    IT[t + 1] = IT[t] + infectionsT - recoveriesT
    RT[t + 1] = RT[t] + recoveriesT

# # Plot the model estimate of the number of infections alongside the data
time = x * dt
pl.plot(time, R, label='Without treatment')
pl.plot(time, RT, label='With treatment')
pl.legend()
pl.title('Recovered people')
pl.show()


