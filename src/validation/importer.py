import csv
import re

from validation.smell import CyclicDependency

from validation.analysis_results import AnalysisResult

ASTRACKER_UNWANTED = ["unstableDep", "hubLikeDep"]
DESIGNITE_UNWANTED = ["Feature Concentration", "Dense Structure", "God Component", "Unstable Dependency", ""]


def extract_cyclic_components(smell_cause):
    smell_list = re.findall("(?:^\w+|\w+\.\w+)+", smell_cause)
    if "The" in smell_list:  # necessary because regex is not working probably
        smell_list.remove("The")
    return smell_list


class FileImporter(object):

    def import_analysis_results(self, path_to_file, commit_sha, consider_version):
        analysis_result = AnalysisResult(commit_sha)
        with open(path_to_file, mode="r") as csv_file:
            for idx, row in enumerate(csv.DictReader(csv_file)):
                # checking for issue is merely an optimization for astracker results
                if consider_version and row["commit_sha"] != commit_sha:
                    continue
                # skip unwanted smells of ASTracker results
                if "smell_type" in row.keys() and row["smell_type"] in ASTRACKER_UNWANTED:
                    continue
                    # skip unwanted smells of ASTracker results
                if "Architecture Smell" in row.keys() and row["Architecture Smell"] in DESIGNITE_UNWANTED:
                    continue
                analysis_result.add_smell(self.convert_csv_row(row, idx))
        return analysis_result

    def convert_csv_row(self, row, smell_id):
        raise Exception("Method not implemented")


class ASTrackerImporter(FileImporter):

    def convert_csv_row(self, row, smell_id):
        smell_type = row["smell_type"]
        smell = None
        if smell_type == "cyclicDep":
            smell = CyclicDependency(row["unique_smell_id"], row["affected_elements"])
        return smell


class DesigniteImporter(FileImporter):

    def convert_csv_row(self, row, smell_id):
        smell_type = row["Architecture Smell"]
        smell = None
        if smell_type == "Cyclic Dependency":
            smell = CyclicDependency(smell_id, extract_cyclic_components(row["Cause of the Smell"]))
        return smell
