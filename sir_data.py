"""
Make some data
"""


# Load packages
import numpy as np
import sciris as sc
import pylab as pl

sc.options(dpi=150)


# Define our parameters
beta = 0.5
gamma = 0.2
npts = 100
I0 = 3
N = 1000
dt = 1

for randomize in [True, False]:
    seed = 1 
    noise = 1.0
    np.random.seed(seed)
    
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
        infections = beta * S[t] * I[t]/N * dt
        if randomize:
            infections = np.random.poisson(infections) # Randomise it
        recoveries = gamma * I[t] * dt
    
        S[t + 1] = S[t] - infections
        I[t + 1] = I[t] + infections - recoveries
        R[t + 1] = R[t] + recoveries
    
    # Plot the model estimate of the number of infections alongside the data
    time = x * dt
    if randomize:
        pl.scatter(time, I, label='Data')
    else:
        pl.plot(time, I, label='Model', c='k')

    pl.legend()
    pl.show()
        
    # Save data
    if randomize:
        df = sc.dataframe(dict(day=time, cases=I))
        df.to_csv('flu_cases.csv')
