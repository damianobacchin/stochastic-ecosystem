import numpy as np
import matplotlib.pyplot as plt
from time import time
import random

from species import chain, ecosystem, init
from species import Animal, Plant


class Model:
    def __init__(self):
        
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

        # Initial state
        self.state = np.zeros(len(self.species))
        for specie, num in init.items():
            self.state[self.species.index(specie)] = num
        
        # GENERATE NETWORK-BASED REACTIONS
        # Eating
        for predator, preys in chain.items():
            for prey in preys:
                self.add_reaction( { predator: 1, prey: 1 }, { prey: -1 }, predator.param )

        # Multiplying
        self.mult_idx = len(self.parameters)
        for specie in self.species:
            self.add_reaction( { specie: 2 }, { specie: 1 }, 1000*specie.growth )
        
        # Starvation
        self.starv_idx = len(self.parameters)
        for specie in self.species:
            if type(specie) == Plant:
                continue
            starv_rate = self.state[self.species.index(specie)] / sum([ self.state[self.species.index(prey)] for prey in chain[specie] ])
            self.add_reaction( { specie: 1 }, { specie: -1 }, starv_rate )
        
        self.products = np.array(self.products)
        self.propensities = np.zeros(len(self.parameters))

    def add_reaction(self, reactants={}, products={}, param=1):
        reaction_reactants = np.zeros(len(self.species))
        reaction_products = np.zeros(len(self.species))
        for specie in reactants.keys():
            reaction_reactants[self.species.index(specie)] = reactants[specie]
        for specie in products.keys():
            reaction_products[self.species.index(specie)] = products[specie]
        self.reactants.append(reaction_reactants)
        self.products.append(reaction_products)
        self.parameters.append(param)

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
            self.parameters[self.starv_idx + i] = self.state[idx] / (sum([ self.state[self.species.index(prey)] for prey in chain[specie] ]) +0.1)
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

        # Simulate drought
        if self.time>0.4:
            for i, plant in enumerate(self.species):
                if type(plant) != Plant:
                    continue
                self.parameters[self.mult_idx + i] = 10 * plant.growth

        # Switch from SSA to Tau Leaping
        if tau > 1/self.a0:
            tx_idx = self.get_next_reaction()
            self.state += self.products[tx_idx]
        else:
            products_vector = self.tau_leaping(tau)
            for i, n_reactions in enumerate(products_vector):
                self.state += self.products[i] * n_reactions

        return self.time, self.state.copy()
    
    # Start the simulation
    def simulate(self, tmax=2):
        times = []
        states = []
        while self.time <= tmax:
            new_time, new_state = self.step()
            times.append(new_time)
            states.append(new_state)
        return np.array(times), np.array(states)


if __name__=='__main__':

    fig, ax = plt.subplots(1, 1)
    get_colors = lambda n: ["#%06x" % random.randint(0, 0xFFFFFF) for _ in range(n)]
    colors = get_colors(len(init.keys()))

    for i in range(5):
        model = Model()
        times, states = model.simulate()
        
        for n, specie in enumerate(model.species):
            ax.plot(times, states.T[n], alpha=0.2, color=colors[n])
            
    plt.legend([specie.name for specie in model.species], loc='best', shadow=True)
    plt.show()