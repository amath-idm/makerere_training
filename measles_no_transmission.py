"""
Model for measles with transmission-bocking treatment
"""


# Load packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as pl 

# Define our parameters
R0 = 17
gamma = 1/25
beta = R0*gamma
delta = 0.2  # treatment rate

# Initial conditions and other settings
npts = 100
I0 = 1
N = 1000
dt = 1

# Make arrays where we will store the estimates
x = np.arange(npts)
S = np.zeros(npts)
I = np.zeros(npts)
T = np.zeros(npts)
R = np.zeros(npts)
Sn = np.zeros(npts)  # Copy of the arrays with no treatment
In = np.zeros(npts)
Rn = np.zeros(npts)

# Initial conditions
S[0] = N - I0
I[0] = I0
Sn[0] = N - I0
In[0] = I0

# Simulate the model over time
for t in x[:-1]:

    infections = beta * S[t] * I[t]/N * dt
    recoveries = gamma * I[t] * dt
    treatments = delta * I[t] * dt
    treatment_recoveries = gamma * T[t] * dt

    infections_nt = beta * Sn[t] * In[t]/N * dt
    recoveries_nt = gamma * In[t] * dt

    S[t + 1] = S[t] - infections
    I[t + 1] = I[t] + infections - recoveries - treatments
    T[t + 1] = T[t] + treatments - treatment_recoveries
    R[t + 1] = R[t] + recoveries + treatment_recoveries

    Sn[t + 1] = Sn[t] - infections_nt
    In[t + 1] = In[t] + infections_nt - recoveries_nt
    Rn[t + 1] = Rn[t] + recoveries_nt

# # Plot the model estimate of the number of infections alongside the data
time = x * dt
pl.plot(time, In, label='Without treatment')
pl.plot(time, I, label='With treatment')
pl.legend()
pl.title('Infectious people')
pl.show()


