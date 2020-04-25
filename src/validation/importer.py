import csv
import re

from validation.smell import CyclicDependency


def import_csv_content(path_to_file):
    with open(path_to_file, mode="r") as csv_file:
        return csv.DictReader(csv_file)


class FileImporter(object):

    def import_analysis_results(self, path_to_file, commit_sha=None):
        # TODO: add analysis report!
        smells = dict()
        with open(path_to_file, mode="r") as csv_file:
            for idx, row in enumerate(csv.DictReader(csv_file)):
                # checking for issue is merely an optimization for astracker results
                if commit_sha is not None and row["commit_sha"] != commit_sha:
                    continue
                smells[idx] = self.convert_csv_row(row, idx)
        return smells

    def convert_csv_row(self, row, smell_id):
        raise Exception("Method not implemented")


class ASTrackerImporter(FileImporter):

    def convert_csv_row(self, row, smell_id):
        smell_type = row["smell_type"]
        smell = None
        if smell_type == "cyclicDep":
            smell = CyclicDependency(row["unique_smell_id"], row["affected_elements"])
        return smell


def extract_cyclic_components(smell_cause):
    smell_list = re.findall("(?:^\w+|\w+\.\w+)+", smell_cause)
    if "The" in smell_list:
        smell_list.remove("The")
    return smell_list


class DesigniteImporter(FileImporter):

    def convert_csv_row(self, row, smell_id):
        smell_type = row["Architecture Smell"]
        smell = None
        if smell_type == "Cyclic Dependency":
            smell = CyclicDependency(smell_id, extract_cyclic_components(row["Cause of the Smell"]))
        return smell
