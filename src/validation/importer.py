import csv


def import_csv_content(path_to_file):
    with open(path_to_file, mode="r") as csv_file:
        return csv.DictReader(csv_file)


class FileImporter(object):

    def import_analysis_results(self, path_to_file):
        csv_file = import_csv_content(path_to_file)
        return self.convert_csv_restults(csv_file)

    def convert_csv_restults(self, csv_file):
        raise Exception("Method not implemented")


class ASTrackerImporter(FileImporter):

    def convert_csv_restults(self, csv_file):
        print("Inside ASTrackerImporter")
