import csv

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
                smells[idx] = self.convert_csv_row(row)
        return smells

    def convert_csv_row(self, csv_file):
        raise Exception("Method not implemented")


class ASTrackerImporter(FileImporter):

    def convert_csv_row(self, row):
        smell_type = row["smell_type"]
        smell = None
        if smell_type == "cyclicDep":
            smell = CyclicDependency(row["unique_smell_id"], row["affected_elements"])
        return smell
