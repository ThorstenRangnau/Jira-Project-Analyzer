from .smell import CyclicDependency


class AnalysisResult(object):

    def __init__(self, version):
        self.version = version
        self.cyclic_dependencies = list()

    def add_smell(self, smell):
        if isinstance(smell, CyclicDependency):
            self.cyclic_dependencies.append(smell)
