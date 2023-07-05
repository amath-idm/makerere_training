"""
Model for COVID-19 lockdowns
"""


# Load packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as pl 

# Define our parameters
R0 = 3.5
gamma = 1/7
beta = R0*gamma
beta_after_lockdown = beta / 2 # Lockdown halves beta

# Initial conditions and other settings
npts = 100
I0 = 1
N = 1000
dt = 1
t_lockdown = 10  # Lockdown on day 10

# Make arrays where we will store the estimates
x = np.arange(npts) 
S = np.zeros(npts)
I = np.zeros(npts)
R = np.zeros(npts)
Sn = np.zeros(npts)  # Copy of the arrays with no lockdown
In = np.zeros(npts)
Rn = np.zeros(npts)

# Initial conditions
S[0] = N - I0
I[0] = I0
Sn[0] = N - I0
In[0] = I0

# Simulate the model over time
for t in x[:-1]:

    if t < t_lockdown:
        infections = beta * S[t] * I[t]/N * dt
        recoveries = gamma * I[t] * dt
    else:
        infections = beta_after_lockdown * S[t] * I[t] / N * dt
        recoveries = gamma * I[t] * dt

    infections_nt = beta * Sn[t] * In[t]/N * dt
    recoveries_nt = gamma * In[t] * dt

    S[t + 1] = S[t] - infections
    I[t + 1] = I[t] + infections - recoveries
    R[t + 1] = R[t] + recoveries

    Sn[t + 1] = Sn[t] - infections_nt
    In[t + 1] = In[t] + infections_nt - recoveries_nt
    Rn[t + 1] = Rn[t] + recoveries_nt

# # Plot the model estimate of the number of infections alongside the data
time = x * dt
pl.plot(time, In, label='Without lockdown')
pl.plot(time, I, label='With lockdown')
pl.legend()
pl.title('Infectious people')
pl.show()


