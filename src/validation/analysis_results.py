class AnalysisResult(object):

    def __init__(self, version, smells):
        self.version = version
        self.smells = smells


class ASTrackerResults(AnalysisResult):

    def __init__(self, version, smells):
        super().__init__(version, smells)


class DesigniteResults(AnalysisResult):

    def __init__(self, version, smells):
        super().__init__(version, smells)
