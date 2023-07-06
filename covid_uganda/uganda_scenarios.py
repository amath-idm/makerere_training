'''
Run Vietnam vaccine scenarios
'''

import numpy as np
import sciris as sc
import covasim as cv
import process_data
import parameters

#%% Set options

do_save = False
cv.options(dpi=150)

start_day = process_data.start_day
end_day   = process_data.end_day

total_pop = sc.loadjson(process_data.popout)['total']

variants = [
    cv.variant(parameters.variants.delta, days='2021-05-25', n_imports=100, label='delta', rescale=False),
    cv.variant(parameters.variants.omicron, days='2022-01-15', n_imports=100, label='omicron', rescale=False),
]


#%% Define interventions

def num_doses(sim): # Because 'data' is not implemented
    doses = np.nanmax([sim.data.dose1.values[sim.t], 0])
    return doses

def num_doses2(sim, shift=30): # Because 'data' is not implemented
    try:
        doses = np.nanmax([sim.data.dose1.values[sim.t+30], 0])
    except:
        doses = 0
    return doses

cb = cv.change_beta(['2021-07-01', '2021-08-20', '2021-10-15', '2022-01-01', '2022-03-10'], [0.2, 0.3, 0.7, 0.4, 0.2], do_plot=False)
tx = cv.test_prob(0.01, start_day=start_day, do_plot=False)
vx = cv.vaccinate_num(parameters.vaccines.pfizer, num_doses=num_doses, sequence='age', do_plot=False)
vx2 = cv.vaccinate_num(parameters.vaccines.pfizer, num_doses=num_doses2, sequence='age', do_plot=False)


#%% Define default parameters and create sims
pars = dict(
    n_agents = 100e3,
    scaled_pop = total_pop,
    pop_infected = 0,
    pop_type = 'hybrid',
    location = 'vietnam',
    start_day = start_day,
    end_day = end_day,
    variants = variants,
)

sim1 = cv.Sim(pars, datafile=process_data.outfile, interventions=[tx, vx, cb], label='Observed')
sim2 = cv.Sim(pars, datafile=process_data.outfile, interventions=[tx, cb], label='No vaccination')
sim3 = cv.Sim(pars, datafile=process_data.outfile, interventions=[tx, vx2, cb], label='Earlier vaccination')


#%% Run
if __name__ == '__main__':
    
    T = sc.timer()

    n_runs = 10
    msim1 = cv.MultiSim(sim1).run(n_runs=n_runs)
    msim2 = cv.MultiSim(sim2).run(n_runs=n_runs)
    msim3 = cv.MultiSim(sim3).run(n_runs=n_runs)
    
    msim1.mean()
    msim2.mean()
    msim3.mean()
    
    mm = cv.MultiSim.merge(msim1, msim2, msim3, base=True)
    mm.plot(['cum_infections', 'cum_deaths'])
    if do_save:
        cv.savefig('vietnam-scenarios.png')

    T.toc('Done')