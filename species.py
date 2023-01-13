class Ecosystem:
    def __init__(self, name):
        self.name = name
        self.species = []
    
    def add_specie(self, specie):
        self.species.append(specie)


class Specie:
    def __init__(self, name, type):
        self.name = name
        self.type = type
        ecosystem.add_specie(self)


class Animal(Specie):
    def __init__(self, name, type, ferocity=False, repletion=False, growth=0):
        super().__init__(name, type)
        self.param = ferocity or repletion
        self.growth = growth


class Plant(Specie):
    def __init__(self, name, growth):
        super().__init__(name, type='plant')
        self.growth = growth



ecosystem = Ecosystem('Ecosystem')

# PREDATOR -> name, type=predator, ferocity, growth
lions = Animal(name='Lions', type='predator', ferocity=.1, growth=.13)
hyenas = Animal(name='Hyenas', type='predator', ferocity=.2, growth=.1)

# PREY -> name, type=prey, repletion, growth
gazelles = Animal(name='Gazelles', type='prey', repletion=.3, growth=.6)
zebre = Animal(name='Zebre', type='prey', repletion=.9, growth=.4)
antelopes = Animal(name='Antelopes', type='prey', repletion=.9, growth=.9)

# PLANT -> name, type=plant, repletion, growth
grass = Plant(name='Grass', growth=0.6)
acacia = Plant(name='Acacia', growth=.3)
ficus = Plant(name='Ficus', growth=.4)


# key -> predator, value -> prey
chain = {
    lions: [gazelles, zebre],
    hyenas: [gazelles, antelopes],
    gazelles: [grass, ficus],
    zebre: [acacia, grass],
    antelopes: [grass]
}

# Initial state (t=0)
init = {
    lions: 10,
    hyenas: 20,
    gazelles: 40,
    zebre: 40,
    antelopes: 60,
    acacia: 40,
    ficus: 40,
    grass: 20
}