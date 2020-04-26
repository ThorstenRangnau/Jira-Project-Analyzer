def extract_participating_components(components):
    participating_components = list()
    for component in components:
        participating_components.append(Component(component))
    return participating_components


class Smell(object):

    def __init__(self, id, components):
        self.id = id
        self.participating_components = extract_participating_components(components)


class CyclicDependency(Smell):

    def __init__(self, id, components):
        super().__init__(id, components)


class Component(object):

    def __init__(self, name):
        self.name = name
