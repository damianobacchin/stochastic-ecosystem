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
gazelles = Animal(name='Gazelles', type='prey', repletion=.3, growth=.6)
antelopes = Animal(name='Antelopes', type='prey', repletion=.7, growth=.3)
grass = Plant(name='Grass', type='plant', growth=0.9)


chain = {
    lions: [gazelles],
    gazelles: [grass],
    antelopes: [grass]
}

init = {
    lions: 10,
    gazelles: 20,
    antelopes: 40,
    grass: 20
}