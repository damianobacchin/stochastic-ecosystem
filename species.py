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
    def __init__(self, name, type, growth):
        super().__init__(name, type)
        self.growth = growth



ecosystem = Ecosystem('Ecosystem')

lions = Animal(name='Lions', type='predator', ferocity=.1, growth=.2)
hyenas = Animal(name='Hyenas', type='predator', ferocity=.2, growth=.1)

gazelles = Animal(name='Gazelles', type='prey', repletion=.6, growth=.7)
zebre = Animal(name='Zebre', type='prey', repletion=.9, growth=.4)
antelopes = Animal(name='Antelopes', type='prey', repletion=.8, growth=.4)

acacia = Plant(name='Acacia', type='plant', growth=.9)
ficus = Plant(name='Ficus', type='plant', growth=.9)
grass = Plant(name='Grass', type='plant', growth=.9)

chain = {
    lions: [gazelles, zebre],
    hyenas: [gazelles, antelopes],
    gazelles: [ficus, grass],
    zebre: [acacia, grass],
    antelopes: [grass]
}

init = {
    lions: 10,
    hyenas: 20,
    gazelles: 40,
    zebre: 40,
    antelopes: 60,
    acacia: 50,
    ficus: 40,
    grass: 20
}