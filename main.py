import numpy as np
import matplotlib.pyplot as plt
from time import time
import random

from species import chain, ecosystem, init
from species import Animal, Plant



class Model:
    def __init__(self):
        # Generate network-based reactions
        self.species = []
        self.reactants = []
        self.products = []
        self.state = []
        self.parameters = []

        self.time = 0.0

        for specie in chain.keys():
            self.species.append(specie)
        for specie in ecosystem.species:
            if type(specie) == Plant:
                self.species.append(specie)

        # Eating
        for predator, preys in chain.items():
            for prey in preys:
                reaction_reactants = np.zeros(len(self.species))
                reaction_products = np.zeros(len(self.species))

                reaction_reactants[self.species.index(predator)] = 1
                reaction_reactants[self.species.index(prey)] = 1
                reaction_products[self.species.index(prey)] = -1

                self.reactants.append(reaction_reactants)
                self.products.append(reaction_products)
                self.parameters.append(predator.param)

        # Multiplying
        for specie in self.species:
            reaction_reactants = np.zeros(len(self.species))
            reaction_products = np.zeros(len(self.species))

            reaction_reactants[self.species.index(specie)] = 2
            reaction_products[self.species.index(specie)] = 1

            self.reactants.append(reaction_reactants)
            self.products.append(reaction_products)
            self.parameters.append(1000 * specie.growth)
        
        # Initial state
        self.state = np.zeros(len(self.species))
        for specie, num in init.items():
            self.state[self.species.index(specie)] = num
        
        # Starvation
        self.starv_idx = len(self.parameters)
        for specie in self.species:
            if type(specie) == Plant:
                continue
            reaction_reactants = np.zeros(len(self.species))
            reaction_products = np.zeros(len(self.species))

            reaction_reactants[self.species.index(specie)] = 1
            reaction_products[self.species.index(specie)] = -1

            self.reactants.append(reaction_reactants)
            self.products.append(reaction_products)
            starv_rate = self.state[self.species.index(specie)] / sum([ self.state[self.species.index(prey)] for prey in chain[specie] ])
            self.parameters.append(starv_rate)
        
        self.products = np.array(self.products)
        self.propensities = np.zeros(len(self.parameters))

    def get_h(self, index):
        reaction = self.reactants[index]
        if sum(reaction) == 0:
            return 1
        elif sum(reaction) == 1:
            return self.state[np.where(reaction == 1)]
        elif sum(reaction) == 2:
            if np.where(reaction == 1):
                return np.prod([ self.state[x] for x in np.where(reaction == 1)[0] ])
            else:
                elem_state = self.state[np.where(reaction == 2)]
                return np.prod([elem_state, elem_state-1, 0.5])

    def update_propensities(self):
        for i, specie in enumerate(self.species):
            if type(specie) == Plant:
                continue
            idx = self.species.index(specie)
            self.parameters[self.starv_idx + i] = self.state[idx] / (sum([ self.state[self.species.index(prey)] for prey in chain[specie] ]) +1)
        for i in range(len(self.parameters)):
            self.propensities[i] = self.get_h(i) * self.parameters[i]
        self.a0 = sum(self.propensities)

    def calc_tau(self):
        return (1/self.a0) * (np.log(1/np.random.uniform()))
    
    def get_next_reaction(self):
        random = self.a0 * np.random.uniform()
        index = 0
        select = 0
        while index<random:
            index += self.propensities[select]
            select += 1
        return select-1
    
    def tau_leaping(self, tau):
        products_vector = []
        for i, reaction in enumerate(self.parameters):
            _lambda = self.propensities[i] * tau
            if _lambda<5:
                n_reactions = np.random.poisson(_lambda)
            else:
                n_reactions = -1
                while n_reactions<0:
                    n_reactions = np.random.normal(_lambda, np.sqrt(_lambda))
            products_vector.append(n_reactions)
        return products_vector

    def step(self):
        self.update_propensities()
        if self.a0 == 0:
            return self.time, self.state.copy()
        tau = self.calc_tau()
        self.time += tau
        if tau>5e-8:
            tx_idx = self.get_next_reaction()
            self.state += self.products[tx_idx]
        else:
            products_vector = self.tau_leaping(tau)
            for i, n_reactions in enumerate(products_vector):
                self.state += self.products[i] * n_reactions

        return self.time, self.state.copy()
    
    def simulate(self, tmax=0.5):
        times = []
        states = []
        while self.time <= tmax:
            new_time, new_state = self.step()
            times.append(new_time)
            states.append(new_state)
        return np.array(times), np.array(states)


if __name__=='__main__':

    fig, ax = plt.subplots(1, 1)

    model = Model()
    times, states = model.simulate()

    for n, specie in enumerate(model.species):
        ax.plot(times, states.T[n], label=specie.name)

    plt.legend(loc='best', shadow=True)
    plt.show()