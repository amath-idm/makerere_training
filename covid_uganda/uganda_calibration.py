'''
Set up the simulation
'''

import numpy as np
import sciris as sc
import covasim as cv
import process_data
import parameters


cv.options(dpi=150)

start_day = process_data.start_day
end_day   = process_data.end_day
total_pop = 45.85e6 # Uganda population size

variants = [
    cv.variant(parameters.variants.delta, days='2021-05-25', n_imports=100, label='delta', rescale=False),
    cv.variant(parameters.variants.omicron, days='2022-01-15', n_imports=100, label='omicron', rescale=False),
]

def num_doses(sim): # Because 'data' is not implemented
    doses = np.nanmax([sim.data.dose1.values[sim.t], 0])
    return doses

tx = cv.test_prob(0.01, start_day=start_day, do_plot=False)
vx = cv.vaccinate_num(parameters.vaccines.pfizer, num_doses=num_doses, sequence='age', do_plot=False)
cb = cv.change_beta(['2021-07-01', '2021-08-20', '2021-10-15', '2022-01-01', '2022-03-10'], [0.2, 0.3, 0.7, 0.4, 0.2], do_plot=False)


pars = dict(
    n_agents = 100e3,
    scaled_pop = total_pop,
    pop_infected = 0,
    pop_type = 'hybrid',
    location = 'uganda',
    start_day = start_day,
    end_day = end_day,
    variants = variants,
    interventions = [tx, vx, cb]
)

sim = cv.Sim(pars, datafile='vietnam_data.csv') # TODO: update

if __name__ == '__main__':
    
    T = sc.timer()

    msim = cv.MultiSim(sim).run(n_runs=3)
    
    to_plot = ['new_infections', 'cum_diagnoses', 'cum_known_deaths', 'new_diagnoses', 'new_known_deaths', 'new_doses']
    msim.mean()
    sim = msim.sims[0]
    fit = sim.compute_fit()
    msim.plot(fig_args=dict(figsize=(16,10)), to_plot=to_plot)
    fit.plot()
    # msim.plot(['new_diagnoses', 'new_known_deaths', 'new_doses'])
    cv.savefig('uganda_calibration.png')
    print(fit.mismatches)
    print(fit.mismatch)
    
    T.toc('Done')