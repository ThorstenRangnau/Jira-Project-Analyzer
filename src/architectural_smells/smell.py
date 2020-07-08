from datetime import datetime

DATE_FORMATTER = '%d-%m-%Y'
CYCLIC_DEPENDENCY = 'CYCLIC_DEPENDENCY'
UNSTABLE_DEPENDENCY = 'UNSTABLE_DEPENDENCY'
HUBLIKE_DEPENDENCY = 'HUBLIKE_DEPENDENCY'


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

    def get_affected_elements(self):
        return [element.name for element in self.affected_elements]


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


class Version(object):

    def __init__(self, commit_sha):
        self.commit_sha = commit_sha
        self.smells_by_type = dict()
        self.smells_by_type[CYCLIC_DEPENDENCY] = dict()
        self.smells_by_type[UNSTABLE_DEPENDENCY] = dict()
        self.smells_by_type[HUBLIKE_DEPENDENCY] = dict()
        self.cyclic_dependencies = None
        self.unstable_dependencies = None
        self.hublike_depenencies = None
        self.date = None
        self.issue_key = None
        self.message = None
        self.url = None
        self.issue_type = None
        self.assignee = None
        self.priority = None
        self.issue_created = None
        self.issue_resolution_date = None
        self.issue_updated = None
        self.resolution_time = None
        self.resolution_status = None
        self.issue_summary = None
        self.comments = None

    def add_commit_information(self, issue_key, message, url):
        self.issue_key = issue_key
        self.message = message
        self.url = url

    def add_smell_numbers(self, cyclic_dependencies, unstable_dependencies, hublike_dependencies):
        self.cyclic_dependencies = int(cyclic_dependencies)
        self.unstable_dependencies = int(unstable_dependencies)
        self.hublike_depenencies = int(hublike_dependencies)

    def get_number_cyclic_dependencies(self):
        return self.cyclic_dependencies

    def get_number_unstable_dependencies(self):
        return self.unstable_dependencies

    def get_number_hublike_dependencies(self):
        return self.hublike_depenencies

    def get_total_smell_number(self):
        return self.get_number_cyclic_dependencies() + self.get_number_unstable_dependencies() + self.get_number_hublike_dependencies()

    def add_smell(self, smell):
        if isinstance(smell, CyclicDependency):
            if smell.unique_smell_id in self.smells_by_type[CYCLIC_DEPENDENCY]:
                raise Exception("Cyclic Dependency Smell instance with id %s already exist" % smell.unique_smell_id)
            self.smells_by_type[CYCLIC_DEPENDENCY][smell.unique_smell_id] = smell
        if isinstance(smell, UnstableDependency):
            if smell.unique_smell_id in self.smells_by_type[UNSTABLE_DEPENDENCY]:
                raise Exception("Unstable Dependency Smell instance with id %s already exist" % smell.unique_smell_id)
            self.smells_by_type[UNSTABLE_DEPENDENCY][smell.unique_smell_id] = smell
        if isinstance(smell, HubLikeDependency):
            if smell.unique_smell_id in self.smells_by_type[HUBLIKE_DEPENDENCY]:
                raise Exception("Hub-Like Dependency Smell instance with id %s already exist" % smell.unique_smell_id)
            self.smells_by_type[HUBLIKE_DEPENDENCY][smell.unique_smell_id] = smell

    def has_cyclic_dependencies(self):
        return True if len(self.smells_by_type[CYCLIC_DEPENDENCY]) > 0 else False

    def has_unstable_dependencies(self):
        return True if len(self.smells_by_type[UNSTABLE_DEPENDENCY]) > 0 else False

    def has_hublike_dependencies(self):
        return True if len(self.smells_by_type[HUBLIKE_DEPENDENCY]) > 0 else False

    def get_cyclic_dependencies(self):
        return self.smells_by_type[CYCLIC_DEPENDENCY]

    def get_unstable_dependencies(self):
        return self.smells_by_type[UNSTABLE_DEPENDENCY]

    def get_hublike_dependencies(self):
        return self.smells_by_type[HUBLIKE_DEPENDENCY]

    def get_date(self):
        if self.has_cyclic_dependencies():
            return list(self.smells_by_type[CYCLIC_DEPENDENCY].values())[0].birth_day
        if self.has_unstable_dependencies():
            return list(self.smells_by_type[UNSTABLE_DEPENDENCY].values())[0].birth_day
        if self.has_hublike_dependencies():
            return list(self.smells_by_type[HUBLIKE_DEPENDENCY].values())[0].birth_day
