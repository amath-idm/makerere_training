"""
Create a simple agent-based model
Structure: SEIR (sus, exposed, infected, recovered)
Agents are defined by their properties:
   * person number
   * disease state
   * propensity for mixing (how much they are likely to mix with other agents)
Population:
   * a collection of agents
Interactions:
   * we will build these up over time, but initially the rules are S+E => E+E
"""

import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt

# Define a population with 1 exposed person
population = pd.DataFrame({"AgentNo": [1],
                           "State": ["E"],
                           "Mixing": [random.uniform(0, 1)]})

# Now add 9 susceptible people to the population
n_pop = 10
for i in range(2, n_pop + 1):
    agent = pd.DataFrame({"AgentNo": [i],
                          "State": ["S"],
                          "Mixing": [random.uniform(0, 1)]})
    population = pd.concat([population, agent])

# Let's look at the agents
print(population)

# Now we need to move them through time
# Let's look at Agent 1 in the model

# First we pull out their propensity of mixing/socialising
mix_1 = population.Mixing.iloc[0]

# Then we use this to determine how many people they'll meet
contacts_1 = round(mix_1 * 3)

# Then we figure out who these people they meet are
contact_nos_1 = np.random.choice(range(1, n_pop + 1), contacts_1, replace=True)
# This tells us that person 1 meets "Contact1" people, and we also know who these people are
# Now let's see what happens at each of these meetings!

# Loop over all of this person's contacts
for j in contact_nos_1:
    # Grab who they meet
    agent = population.iloc[j - 1]
    # If they meet someone who's exposed, then they become exposed
    if agent["State"] == "E":
        population.State.iloc[0] = "E"

# We need to do this for everyone in the model: let's make another loop.
for i in range(n_pop):
    # First we pull out this person's propensity of mixing/socialising
    mix = population.Mixing.iloc[i]
    # Then we use this to determine how many people they'll meet
    contacts = round(mix * 3)
    # Then we figure out who these people they meet are
    contact_nos = np.random.choice(range(1, n_pop + 1), contacts, replace=True)
    # Did they meet anyone?
    if len(contact_nos) > 0:
        # Now let's see what happens at each of these meetings!
        for j in contact_nos:
            # Grab who they meet
            agent = population.iloc[j - 1]
            # If they meet someone who's exposed, then they become exposed
            if agent["State"] == "E":
                population.State.iloc[i] = "E"

# Let's look at the population again
print(population)

# Lots of people have become exposed!
# Eventually, everyone is exposed
# An easier way to see this is to look at a summary table.
state_counts = population["State"].value_counts()
print(state_counts)

# Let's make it a little more realistic. We'll remake the population and
# take the same code as we used above, but now we'll incorporate the info
# about how likely people are to mix
population = pd.DataFrame({"AgentNo": [1],
                           "State": ["E"],
                           "Mixing": [random.uniform(0, 1)]})
n_pop = 100
for i in range(2, n_pop + 1):
    agent = pd.DataFrame({"AgentNo": [i],
                          "State": ["S"],
                          "Mixing": [random.uniform(0, 1)]})
    population = pd.concat([population, agent])

# Now we'll simulate what happens over a few timesteps
for t in range(5):
    for i in range(n_pop):
        # First we pull out this person's propensity of mixing/socialising
        mix = population.Mixing.iloc[i]
        # Then we use this to determine how many people they'll meet
        contacts = round(mix * 3) + 1  # CHANGE 1: everyone meets at least 1 person
        # Then we figure out who these people they meet are - CHANGE 2, we used moxing probabilities here
        normalized_mixing = population.Mixing.to_numpy() / sum(population.Mixing.to_numpy())
        contact_nos = np.random.choice(range(1, n_pop + 1), contacts, replace=True, p=normalized_mixing)
        # Did they meet anyone?
        if len(contact_nos) > 0:
            # Now let's see what happens at each of these meetings!
            for j in contact_nos:
                # Grab who they meet
                agent = population.iloc[j - 1]
                # If they meet someone who's exposed, then they become exposed
                if agent["State"] == "E":
                    population.State.iloc[i] = "E"

    state_counts = population["State"].value_counts()
    print(t)
    print(state_counts)

# After a few steps, nearly everyone is exposed! Let's look at the remaining susceptibles
population[population.State == "S"]
# Often, it's people with low mixing parameters that avoid exposure

#################################################
# Simulating the agent-based model over time
#################################################

# Here we define a function that generates our population
def PopGen(nPop, E0, I0):
    Population = pd.DataFrame({'AgentNo': np.arange(1, nPop + 1),
                               'State': 'S',
                               'Mixing': np.random.uniform(0, 1, nPop),
                               'TimeE': 0,
                               'TimeI': 0})

    Population.loc[0:E0 - 1, 'State'] = 'E'
    Population.loc[0:E0 - 1, 'TimeE'] = np.random.binomial(13, 0.5, E0) + 1

    Population.loc[E0:E0 + I0 - 1, 'State'] = 'I'
    Population.loc[E0:E0 + I0 - 1, 'TimeI'] = np.random.binomial(12, 0.5, I0) + 1

    return Population


nPop = 100
myPop = PopGen(nPop, E0=2, I0=3)

par = pd.DataFrame({'MaxMix': [10],
                    'S2E': [0.25],
                    'E2I': [0.1],
                    'I2D': [0.05]})


def ABM(Population, par, nTime):
    nPop = len(Population)
    Out = pd.DataFrame({'S': np.zeros(nTime),
                        'E': np.zeros(nTime),
                        'I': np.zeros(nTime),
                        'R': np.zeros(nTime),
                        'D': np.zeros(nTime)})

    for k in range(nTime):
        StateS1 = Population[Population['State'] == 'S'].index
        StateSE1 = Population[(Population['State'] == 'S') | (Population['State'] == 'E')].index

        for i in StateS1:
            Mix = Population.loc[i, 'Mixing']
            Contacts = round(Mix * par['MaxMix'][0]) + 1
            ContactNos = random.choices(StateSE1, k=Contacts, weights=Population.loc[StateSE1, 'Mixing'])

            for j in range(len(ContactNos)):
                Agent = Population.loc[ContactNos[j]]

                if Agent['State'] == 'E':
                    Coin = random.uniform(0, 1)
                    if Coin < par['S2E'][0]:
                        Population.loc[i, 'State'] = 'E'

        StateE1 = Population[Population['State'] == 'E'].index
        Population.loc[StateE1, 'TimeE'] += 1
        StateE2 = Population[(Population['State'] == 'E') & (Population['TimeE'] > 14)].index
        Population.loc[StateE2, 'State'] = 'R'

        StateE3 = Population[(Population['State'] == 'E') & (Population['TimeE'] > 3)].index
        for i in StateE3:
            Coin = random.uniform(0, 1)
            if Coin < par['E2I'][0]:
                Population.loc[i, 'State'] = 'I'

        StateI1 = Population[Population['State'] == 'I'].index
        Population.loc[StateI1, 'TimeI'] += 1
        StateI2 = Population[(Population['State'] == 'I') & (Population['TimeI'] > 14)].index
        Population.loc[StateI2, 'State'] = 'R'
        StateI3 = Population[(Population['State'] == 'I') & (Population['TimeI'] < 15)].index

        Population.loc[StateI3, 'State'] = np.where(
            np.random.uniform(0, 1, len(StateI3)) > par['I2D'][0], 'I', 'D')

        Out.loc[k, 'S'] = len(Population[Population['State'] == 'S'])
        Out.loc[k, 'E'] = len(Population[Population['State'] == 'E'])
        Out.loc[k, 'I'] = len(Population[Population['State'] == 'I'])
        Out.loc[k, 'R'] = len(Population[Population['State'] == 'R'])
        Out.loc[k, 'D'] = len(Population[Population['State'] == 'D'])

    return Out


Population = PopGen(1000, E0=5, I0=2)
par = pd.DataFrame({'MaxMix': [5],
                    'S2E': [0.15],
                    'E2I': [0.1],
                    'I2D': [0.01]})

Model1 = ABM(Population, par, nTime=25)

# Plot results
Model1['t'] = np.arange(1, 26)
output_long = pd.melt(Model1, id_vars='t')
plt.figure(figsize=(8, 6))
plt.plot(output_long['t'], output_long['value'], marker='o', linestyle='-', linewidth=2)
plt.xlabel('Time (days)')
plt.ylabel('Number of people')
plt.legend(output_long['variable'].unique())
plt.show()
