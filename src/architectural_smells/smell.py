from datetime import datetime


DATE_FORMATTER = '%d-%m-%Y'


def extract_participating_elements(affected_elements):
    participating_elements = list()
    for element in affected_elements:
        participating_elements.append(Element(element))
    return participating_elements


class Smell(object):

    def __init__(self,
                 unique_smell_id,
                 birth_day,
                 version,
                 affected_elements,
                 size):
        self.unique_smell_id = unique_smell_id
        self.birth_day = datetime.strptime(birth_day, DATE_FORMATTER)
        self.version = version
        self.affected_elements = extract_participating_elements(affected_elements)
        self.size = size


class CyclicDependency(Smell):

    def __init__(self,
                 unique_smell_id,
                 birth_day,
                 version,
                 affected_elements,
                 size,
                 shape):
        super().__init__(unique_smell_id,
                         birth_day,
                         version,
                         affected_elements,
                         size)
        self.shape = shape


class UnstableDependency(Smell):

    def __init__(self,
                 unique_smell_id,
                 birth_day,
                 version,
                 affected_elements,
                 size,
                 instability_gap,
                 doud):
        super().__init__(unique_smell_id,
                         birth_day,
                         version,
                         affected_elements,
                         size)
        self.instability_gap = instability_gap
        self.doud = doud


class HubLikeDependency(Smell):

    def __init__(self,
                 unique_smell_id,
                 birth_day,
                 version,
                 affected_elements,
                 size,
                 avrg_internal_path_length,
                 affected_classes_ratio):
        super().__init__(unique_smell_id,
                         birth_day,
                         version,
                         affected_elements,
                         size)
        self.avrg_internal_path_length = avrg_internal_path_length
        self.affected_classes_ratio = affected_classes_ratio


class Element(object):

    def __init__(self, name):
        self.name = name
